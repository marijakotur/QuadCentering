%% Quad alignment
clear all
close all

dir = '/mxn/groups/operators/controlroom/Marija';

save_all_images = false;

% Camera to pull data from
% cam = 'lima/liveviewer/i-bc2-dia-scrn-02';
% cam = 'lima/liveviewer/i-bc2-dia-scrn-03';
% cam = 'lima/liveviewer/i-ms2-dia-scrn-01';
bpm = 'I-BC1/DIA/BPL-02';
% corr = 'I-KBC2/MAG/PSIA-04'; %CODX4
%corr = 'I-KBC1/MAG/PSIA-07';
%corr = 'I-KBC1/MAG/PSIA-03';
%corr = 'I-KBC1/MAG/PSIA-01';
% quad = 'I-KBC2/MAG/PSPG-01-CAB07';
%quad = 'I-KBC1/MAG/PSPB-07';
%quad = 'I-KBC1/MAG/PSPB-07';
% quad = 'I-KBC1/MAG/PSPB-05';

% % the first quad
% cam = 'lima/liveviewer/i-ms1-dia-scrn-01';
% quad = 'I-K01/MAG/PSPB-02';
% corr = 'I-K00/MAG/PSIA-18';

% the 3ed and the 4th quad
cam = 'lima/liveviewer/i-ms1-dia-scrn-01';
quad = 'I-K01/MAG/PSPB-04';
corr = 'I-K01/MAG/PSIA-01';

% % the first quad in MS1
% cam = 'lima/liveviewer/i-ms1-dia-scrn-01';
% quad = 'I-KBC1/MAG/PSPB-01';
% corr = 'I-K01/MAG/PSIA-07';

% tango_write_attribute(cam, 'Gain', 10);
% tango_write_attribute(cam, 'Exposure', 1e-3*50);

% getfield(tango_read_attribute(cam, 'Exposure'),'value')
bpm_initial_X = getfield(tango_read_attribute(bpm, 'X'),'value');
bpm_initial_Y = getfield(tango_read_attribute(bpm, 'Y'),'value');


bkgnd_img = load([dir '/bkgnd_image.mat'],'-mat','img');
bkgnd_img = bkgnd_img.img;
% bkgnd_img = double(bkgnd_img);
if save_all_images
    imwrite(bkgnd_img,['img_bkgnd.png']);
end

    

%check image
% img = getfield(tango_read_attribute(cam, 'Image'), 'value');
% img = img-bkgnd_img;
% save('bkgnd_image','img')
% imagesc(bkgnd_img)
% imagesc(img)

corr_dir_index = 2;  % 1 == x direction
% 2 == y direction
shots_to_avg = 3;

corr_value_initial = getfield(tango_read_attribute(corr,'Current'),'value');
corr_value_initial = corr_value_initial(1);
corr_scan_min = corr_value_initial -0.25;
corr_scan_max = corr_value_initial + 0.25;
% corr_scan_min = -0.2;
% corr_scan_max = 0.2;

corr_scan_points = 4;
corr_scan_values = linspace(corr_scan_min,corr_scan_max,corr_scan_points);

quad_value_initial = getfield(tango_read_attribute(quad,'Current'),'value');
quad_value_initial = quad_value_initial(1);
quad_scan_min = quad_value_initial + 0.2;
quad_scan_max = quad_value_initial + 0.7;
quad_scan_points = 3;
quad_scan_values = linspace(quad_scan_min,quad_scan_max,quad_scan_points);

cm=hsv(length(corr_scan_values));
line_styles = ['d','>','o','d','<','h','-',':','-.','--'];
figure(3)
hold on
% figure(4)
% hold on
str1 = {};
for i=1:length(corr_scan_values)
    tango_write_attribute(corr, 'Current', corr_scan_values(i));
    pause(0.25)
    for j=1:length(quad_scan_values)
        tango_write_attribute(quad, 'Current', quad_scan_values(j));
        pause(0.5)
        lineout = [];
        for k=1:shots_to_avg
            pause(0.5)
            img = getfield(tango_read_attribute(cam, 'Image'), 'value');
%             img=double(img);
            if save_all_images
                imwrite(img,['img_' num2str(i) '_' num2str(j) '_' num2str(k) '.png']);
            end
            img=img-bkgnd_img;
            img = img(100:end-100,100:end-100);
            if k==1
                lineout = mean(img,corr_dir_index);
            else
                lineout = (lineout*(k-1)+mean(img,corr_dir_index))/k;
            end
        end
        figure(3)
        plot(lineout,'color',cm(i,:))
        
        %% make the lineout a vector
        if size(lineout,2) == 1
            lineout = transpose(lineout);
        end
        
        %         %% simple peak detection
        %         x_peak_position(i,j) = find(lineout/max(lineout)==1,1,'first');
        
        
        %% fit gaussian to the lineout
        init = [1, find(lineout/max(lineout)==1,1,'first'), 40, 1];
        
        fit = fitcurve_gaussian(1:length(lineout),lineout/max(lineout),init);
        x_peak_position(i,j) = fit(2);
        
        %%
        str{i,j} = [num2str(corr_scan_values(i)) ' A, ' num2str(quad_scan_values(j)) ' A'];
    end
end

xlabel('Position [pixel]')
ylabel('Sum signal')
legend( reshape(str,length(quad_scan_values)*length(corr_scan_values),[]))

tango_write_attribute(quad, 'Current', quad_value_initial);
tango_write_attribute(corr, 'Current', corr_value_initial);


figure(4)
hold on
for i = 1:length(corr_scan_values)
    str1{i} = [num2str(corr_scan_values(i)) ' A'];
    plot(quad_scan_values,x_peak_position(i,:),'color',cm(i,:),'marker','o')
    
    %% linear fit for each plot
    linfit = polyfit(quad_scan_values,x_peak_position(i,:),1);
    slope(i) = linfit(1);
end

xlabel(['Quad ' quad ' current [A]'])
ylabel('Peak position [pixel]')
title([corr ' current scan']);
legend(str1)

figure(5)
hold on
plot(corr_scan_values,slope,'-o')
xlabel(['Corr ' corr ' current [A]'])
ylabel('Quad current scan slope [arb.]')
% linear fit to find the zero crossing
linfit2 = polyfit(corr_scan_values,slope,1);
plot(corr_scan_values,linfit2(1)*corr_scan_values+linfit2(2),'r--')
new_corrector_setting = -linfit2(2)/linfit2(1);
plot(new_corrector_setting,0,'x')
legend('slope data','fit','new corrector setting','location','best')

disp(['New corrector setting ' num2str(new_corrector_setting) ' A'])

% tango_write_attribute(corr, 'Current', new_corrector_setting);



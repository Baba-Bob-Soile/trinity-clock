filename = 'tilt_49_60_batt_smooth.txt';
name=strtok(filename,'.');
delimiterIn = ' ';
headerlinesIn = 1;
fs=16;

fid=fopen(filename,'r');
C=textscan(fid, '%f%s%s%f%f%f%f', 'Headerlines',1);
unixtime=cell2mat(C(:,1));
date_time=datetime(unixtime,'ConvertFrom','posixtime') ;
date_time.Format = 'dd-MMM-yyyy HH:mm:ss.SSS';
data=cell2mat(C(:,4:7));
inst_data=data(:,1);
t=unixtime-unixtime(1,:);

% windowWidth = 3; % Whatever you want.
% kernel = ones(windowWidth,1) / windowWidth;
% %inst_smooth = filter(kernel, 1, inst_data);
% inst_smooth_two = conv(inst_data,kernel, 'same');
% plot(t, [inst_smooth inst_smooth_two]);
% grid on
figure
grid on
% name=strtok(filename,'.');
% pic_name=strcat(name,'.fig');
% saveas(gcf,pic_name);
%f_data= fft(data(:,1));
f_data= fft(inst_data);
n = length(f_data);          % number of samples
f = (0:n-1)*(fs/n);     % frequency range
f=f';
plot(f,abs(f_data))
xlabel('Frequency(Hz)')
ylabel('FFT Values')
title('FFT of Tilt Before Filtering')
pic_name=strcat(name,'_fft.fig');
saveas(gcf,pic_name);

figure
[B,A]=butter(4,0.1);
inst_filter=filtfilt(B,A,inst_data);
filt_data= fft(inst_filter);
plot(f,abs(filt_data))
xlabel('Frequency (Hz)')
ylabel('FFT Values')
title('FFT of Tilt After Filtering')
pic_name=strcat(name,'_fft_filt.fig');
saveas(gcf,pic_name);

figure
windowWidth = 3*fs; % Whatever you want.
kernel = ones(windowWidth,1) / windowWidth;
inst_smooth= conv(inst_data,kernel, 'same');
%plot(t,inst_data,'b',t,inst_filter,'r', t, inst_smooth,'g')
plot(date_time,inst_data,'b',date_time,inst_filter,'r', date_time, inst_smooth,'g')
xlabel('Time')
ylabel('Tilt (V)')
title('Filtering')
legend('instantaneous','filter','3 sec mov. ave.')
pic_name=strcat(name,'.fig')
saveas(gcf,pic_name);

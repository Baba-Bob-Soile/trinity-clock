filename = 'rigid_one_eighth_turn_a_.txt';
name=strtok(filename,'.');
delimiterIn = ' ';
headerlinesIn = 1;
fid=fopen(filename,'r');
C=textscan(fid, '%f%f%f', 'Headerlines',1);
frame=cell2mat(C(:,1));
time= frame/150*5;
fs=30
x_coord=cell2mat(C(:,2));
y_coord=cell2mat(C(:,3));
figure
plot(time, x_coord)
grid on
figure
plot(time, y_coord)
grid on

figure
f_data=fft(x_coord);
n = length(f_data);          % number of samples
f = (0:n-1)*(fs/n);
f=f';
plot(f,abs(f_data))
grid on
xlabel('Frequency(Hz)')
ylabel('FFT Values')
title('FFT of Tilt Before Filtering')

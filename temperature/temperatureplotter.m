filename = '2017-03-17.txt';
name=strtok(filename,'.');

fid=fopen(filename,'r');
C=textscan(fid, '%f%f%f%f%f%f%f', 'Headerlines',1);
unixtime=cell2mat(C(:,1));
date_time=datetime(unixtime,'ConvertFrom','posixtime') ;
date_time.Format = 'dd-MMM-yyyy HH:mm:ss.SSS';
data=cell2mat(C(:,2:7));


% grid on
figure
grid on



%plot(t,inst_data,'b',t,inst_filter,'r', t, inst_smooth,'g')
plot(date_time,data)
xlabel('Time')
ylabel('Temperature (degree Celsius)')
title('Temperature in pendulum cavity vs Time')
Probe=[1 2 3 4 5 6];
legendCell = cellstr(num2str(Probe', 'Probe %-d'));
legend(legendCell);
pic_name=strcat(name,'.fig');
saveas(gcf,pic_name);

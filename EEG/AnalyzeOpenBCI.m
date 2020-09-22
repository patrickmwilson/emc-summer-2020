%%
test = readtable('Z:\Science Groups\VR-EEG Group\Chris\OpenBCI\EricRT\OpenBCI-RAW-2019-10-25_16-27-50.txt');
Fs = 250; dt = 1/Fs;
timestamps = dt*(1:size(test, 1));
eyesClosedStart = 2; eyesClosedEnd = 32; eyesOpenStart = 32; eyesOpenEnd = 62;
for i = 5%2:size(test,2)-6
    data = table2array(test(:, i));
    if(sum(data==-187500.02) < size(test,1)/2)
     i
    [pxx, f] = pwelch(data(eyesOpenStart*Fs:eyesOpenEnd*Fs), 5000, 2500, 0:0.1:Fs/2, Fs);
    plot(f, db(pxx));
    xlim([0.1 50]);
    hold on
    [pxx, f] = pwelch(data(eyesClosedStart*Fs:eyesClosedEnd*Fs), 5000, 2500, 0:0.1:Fs/2, Fs);
    plot(f, db(pxx));
    legend({'Eyes Open', 'Eyes Closed'});
    title('Chandan Eyes Open Eyes Closed OpenBCI');
    xlabel('Frequency (Hz'); ylabel('Power (dB)');
    end
end
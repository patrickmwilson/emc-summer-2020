function [c1] = defaultWSSTPlotNew( x, y, Fs, varargin )
%DEFAULTWSSTPLOT Makes a wsst plot with the most common parameters in the
%Arisaka lab

%   x is an nx1 time vector, and y is an nx1 data vector, where n is the
%   number of points in the 1D data time-series. Fs is the sampling rate

% plot raw trace and various band-pass filters of the raw trace in upper
% plot

FigH = figure('Position', get(0, 'Screensize'));
y = y - mean(y);
%% Upper plot

% set up axes
plot1 = subplot(2, 1, 1);
set(plot1, 'OuterPosition', [0, 0.7, 1, 0.3]);

% pass bands is a nx2 numeric array specifying the bandpass frequencies
% that will be displayed on the top plot in addition to the raw trace, where
% n is the number of different passbands.
% Each additional passband range is specified in a separate row. A value of
% 0 in the first column indicates a lowpass, and 0 in the second column
% indicates a highpass

hold(plot1, 'on');

% set up variables to hold bandpass filtered traces
y = double(y);

    for i=1:Fs/2/60-1
    [b,a] = butter(2, [i*60-1,i*60+1]/(Fs/2), 'stop');
    y = filtfilt(b, a, y);
    end

% plot the raw trace
plot(plot1, x,y, 'Color', 'black');
title('LFP','FontSize',20)
xlim([x(1) x(end)]);
%% Lower plot

% set up axes
plot2 = subplot(2, 1, 2);
set(plot2, 'OuterPosition', [0, 0, 1, 0.70]);

% set up 100 log-spaced scales to calculate wsst over
scales = logspace(0, log10(Fs), 100);

% compute cfs
[cfs,frequencies] = wsst(y,Fs);
%[cfs,frequencies] = cwt(y,scales,'cmor1-1.5',1/Fs);


% take the real part
c= real(cfs);
c1=c;
% convert color to log scale
 Vmax=max(max(abs(real(c))));
 c1=c/Vmax;
negIndex=find(c1<-1/100);
posIndex=find(c1> 1/100);
zerIndex=find(-1/100 <= c1 & c1 <= 1/100);
c1(negIndex)=-log10(100*abs(c1(negIndex)));
c1(posIndex)=log10(100*abs(c1(posIndex)));
c1(zerIndex)=0;

% make color plot
pc = pcolor(plot2, x,frequencies,c1/2);
grid on; shading interp; 
set(pc, 'EdgeColor', 'none');
os = get(gca, 'Position');

% set up jet edit colorscale (center green changed to white)
ncol=128;
ColorInit=jet(ncol);
jetEdit=[ColorInit([1:ncol/2],:);[1 1 1];ColorInit([ncol/2+1:ncol],:)];

% set color scale to jet edit
colormap(jet);

% add colorbar
cbh=colorbar;
set(gca, 'Position', os);

%xlabel(cbh,sprintf('\\muV'));

% create array of y-tick labels
ytickArray = [1.25]; 
ylimits = ylim(gca);
while ytickArray(end) <= ylimits(2)/2
    ytickArray(end+1) = ytickArray(end)*2;
end
plot2.YTick = ytickArray;
set(gca, 'YScale', 'log');
ylim([1.25, 40]);

xlabel('Time (s)', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('Frequency (Hz)', 'FontSize', 12, 'FontWeight', 'bold');
end


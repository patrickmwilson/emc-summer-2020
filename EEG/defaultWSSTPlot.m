function [c1] = defaultWSSTPlot( x, y, Fs, varargin )
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

passBands = [1, 3.5; 3.5, 7; 7, 14; 14, 28; 28, 56; 56, 112; 112, 0];

% colors is a nx3 numeric array of colors
colors = [0, 0.4470, 0.7410; 0.8500, 0.3250, 0.0980; 0.9290, 0.6940, 0.1250;
    0.4940, 0.1840, 0.5560; 0.4660, 0.6740, 0.1880; 0.3010, 0.7450, 0.9330;
    0.6350, 0.0780, 0.1840];

legendLabels = {'Delta', 'Theta', 'Alpha', 'Beta', 'Slow Gamma', 'Mid Gamma', 'Fast Gamma', 'Raw'};

hold(plot1, 'on');

% set up variables to hold bandpass filtered traces
y = double(y);
filteredData = zeros(size(passBands, 1), length(y));
filterCoefficients = {}; %zeros(size(passBands, 1), 2);

% calculate third-order butterworth filter coefficients for each pass band
% specified
for i = 1:size(passBands, 1)
    if (passBands(i, 1) == 0 && passBands(i, 2) == 0)|| (passBands(i,1) < 0 && passBands(i,2) < 0)
        continue
    elseif passBands(i,1) == 0
            [filterCoefficients{i,1}, filterCoefficients{i,2}] = butter(3, passBands(i, 2)/(0.5*Fs), 'low');
    elseif passBands(i, 2) == 0
            [filterCoefficients{i,1}, filterCoefficients{i,2}] = butter(3, passBands(i, 1)/(0.5*Fs), 'high');
    else
        [filterCoefficients{i,1}, filterCoefficients{i,2}] = butter(3, [passBands(i,1), passBands(i, 2)]/(0.5*Fs));
    end
end

% apply each zero phase filter to the raw data
for i = 1:size(passBands, 1)
    filteredData(i, :) =filtfilt(filterCoefficients{i,1},filterCoefficients{i,2},y);
end

% plot each pass band
for i = 1:size(passBands, 1)
    plot(plot1, x, filteredData(i,:), 'Color', colors(i,:));
end

% plot the raw trace
plot(plot1, x,y, 'Color', 'black');

legend(legendLabels, 'Location', 'northeast');

xlim([x(1) x(end)]);
%% Lower plot

% set up axes
plot2 = subplot(2, 1, 2);
set(plot2, 'OuterPosition', [0, 0, 1, 0.70]);

% set up 100 log-spaced scales to calculate wsst over
scales = logspace(0, log10(Fs), 100);

% compute cfs
[cfs,frequencies] = wsst(y,Fs);

% take the real part
c= real(cfs);

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
ylim([1.25, ylimits(2)]);

xlabel('Time (s)', 'FontSize', 12, 'FontWeight', 'bold');
ylabel('Frequency (Hz)', 'FontSize', 12, 'FontWeight', 'bold');
end


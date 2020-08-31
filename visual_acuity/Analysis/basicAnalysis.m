% Basic analysis

experiments = struct('name', NaN, 'color', NaN, 'fileName', NaN);
experiments = repmat(experiments,1,4);

experiments(1).name = "Isolated Character";
experiments(1).color = 'r';
experiments(1).fileName = "C:\Users\ArisakaLab\Desktop\SAMPLE_01-20_Isolated Character.csv";

experiments(2).name = "Crowded Periphery";
experiments(2).color = 'g';
experiments(2).fileName = "C:\Users\ArisakaLab\Desktop\SAMPLE_01-21_Crowded Periphery.csv";

experiments(3).name = "Crowded Periphery Outer";
experiments(3).color = 'b';
experiments(3).fileName = "C:\Users\ArisakaLab\Desktop\SAMPLE_01-21_Crowded Periphery Outer.csv";

experiments(4).name = "Crowded Periphery Inner";
experiments(4).color = 'k';
experiments(4).fileName = "C:\Users\ArisakaLab\Desktop\SAMPLE_01-27_Crowded Periphery Inner.csv";

txt = "%s: y = %4.2fx + %4.2f";

figure();
hold on;
for i = 1:length(experiments)
    experiment = experiments(i);
    table = readtable(experiment.fileName);
    data = table2array(table);
    
    xvals = data(:,3)';
    yvals = data(:,2)';
    
    params = polyfit(xvals,yvals,1);
    xfit = linspace(min(xvals),max(xvals));
    yfit = polyval(params, xfit);
    
    scatter(xvals, yvals, 20, experiment.color, "filled", 'HandleVisibility', 'off');
    
    plot(xfit, yfit, 'Color', experiment.color, 'LineWidth', 1, 'DisplayName', ...
            sprintf(txt, experiment.name, params(1,1), params(1,2)));
    
end

legend('show', 'Location', 'best');
xlabel("Retinal eccentricity (degrees)");
ylabel("Threshold letter height (degrees)");
title("Retinal eccentricity vs. Threshold letter height");
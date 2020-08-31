

function pointSlope(data, slope, intercept, color, experimentName, fig)

    figure(fig);

    errorbar(data(:,1), data(:,2), data(:,3), 'horizontal','.', ...
            'HandleVisibility', 'off', 'Color', 'k', ...
            'CapSize', 0);
        
    hold on;
    scatter(data(:,1),data(:,2),30,color,'filled','HandleVisibility','off');


    xfit = linspace(0, max(data(:,1)));
    
    yfit = (xfit*slope)+intercept;
    
    if intercept == 0
        txt = "%s: y = %4.3fx";
        
        plot(xfit, yfit, 'Color', color, 'LineWidth', 1, 'DisplayName', ...
            sprintf(txt, experimentName, slope));
    else
        txt = "%s: y = %4.3fx + %4.3f";
        
        plot(xfit, yfit, 'Color', color, 'LineWidth', 1, 'DisplayName', ...
            sprintf(txt, experimentName, slope, intercept));
    end

    legend('show', 'location', 'best');

    xlabel("Retinal Eccentricity (degrees)");
    ylabel("Threshold Letter Height (degrees)");
    title("Threshold Letter Height vs. Retinal Eccentricity");

end
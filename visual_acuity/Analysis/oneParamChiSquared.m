
function oneParamOutput = oneParamChiSquared(data, experimentName, id, color, oneParamGraph, oneParamChiGraph, oneParamOutput)

    xvals = data(:,1)';
    yvals = data(:,2)';
    sErrors = data(:,4)';

    sErrors(sErrors == 0) = 0.00000001;

    weights = 1./sErrors;

    f = @(x, xvals, yvals, weights)sum((weights.*((yvals-(xvals.*x))).^2));
    fun = @(x)f(x, xvals, yvals, weights);

    [slope, oneParamChi] = fminbnd(fun, 0, 1);
    
    oneParamOutput.(strcat(id, '_slope')) = slope;
    oneParamOutput.(strcat(id, '_chi_sq')) = oneParamChi;
    
    
    oneParamReducedChi = oneParamChi/(length(xvals)-1);
    
    oneParamOutput.(strcat(id, '_reduced_chi_sq')) = oneParamReducedChi;

    pointSlope(data, slope, 0, color, experimentName, ...
        oneParamGraph);
    
    % -----------------------------------
    
    figure(oneParamChiGraph);
    hold on;
    
    evals = linspace((slope*0.5),(slope*1.5));
    
    chi = cellfun(fun, num2cell(evals));
    
    chisqtext = "\chi^{2}"; 
    redchisqtext = "\chi^{2}_{v}";
    
    txt = "%s min: %4.2f, %s: %4.2f, Slope: %4.3f";
    
    plot(evals, chi, 'Color', color, 'LineWidth', 1, 'DisplayName', ...
        sprintf(txt, chisqtext, oneParamChi, redchisqtext, oneParamReducedChi, slope));
    
    yline = ones(length(evals)).*(oneParamChi+1);
    plot(evals, yline, 'Color', [1 0 0], 'LineWidth', 1, ...
        'HandleVisibility', 'off');
    
    legend('show', 'Location', 'best');
    
    xlabel('Slope');
    ylabel(chisqtext);
    
    titletxt = "%s vs. Slope";
    title(sprintf(titletxt, chisqtext));
    
    xlim([0 max(evals*1.5)]);
    ylim([0 ((oneParamChi+1)*2)]);
    
    target = oneParamChi + 1;
    
    f = @(x, xvals, yvals, weights)abs(target-(sum((weights.*((yvals-(xvals.*x))).^2))));
    fun = @(x)f(x, xvals, yvals, weights);
    
    negError = slope - fminbnd(fun, (slope*0.5), slope);
    posError = fminbnd(fun, slope, (slope*1.5)) - slope;
    
    oneParamOutput.(strcat(id, '_neg_error')) = negError;
    oneParamOutput.(strcat(id, '_pos_error')) = posError;

end
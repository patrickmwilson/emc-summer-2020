

function twoParamOutput = twoParamChiSquared(data, experimentName, id, color, twoParamGraph, twoParamChiGraph, twoParamOutput)

    xvals = data(:,1)';
    yvals = data(:,2)';
    sErrors = data(:,4)';

    sErrors(sErrors == 0) = 0.00000001;

    weights = 1./sErrors;

    f = @(x, xvals, yvals, weights)sum(weights.*((yvals-((xvals.*x(1))+x(2))).^2));
    fun = @(x)f(x,xvals,yvals,weights);

    approx = polyfit(xvals, yvals, 1);

    ms = MultiStart;
    problem = createOptimProblem('fmincon','x0',approx, ...
        'objective', fun, 'lb', [0, -1], 'ub', [1,1]);

    params = run(ms, problem, 50);

    slope = params(1);
    intercept = params(2);
    
    twoParamOutput.(strcat(id, '_slope')) = slope;
    twoParamOutput.(strcat(id, '_intercept')) = intercept;

    twoParamChi = fun(params);
    
    twoParamOutput.(strcat(id, '_chi_sq')) = twoParamChi;

    twoParamReducedChi = twoParamChi/(length(xvals)-2);
    
    twoParamOutput.(strcat(id, '_reduced_chi_sq')) = twoParamReducedChi;

    pointSlope(data, slope, intercept, color, experimentName, ...
        twoParamGraph);
    
    target = twoParamChi + 1;
    
    f = @(x, intercept, xvals, yvals, weights)abs(target-sum(weights.*((yvals-((xvals.*x)+intercept)).^2)));
    fun = @(x)f(x, intercept, xvals, yvals, weights);
    
    negSlopeError = fminbnd(fun, (slope*0.5), slope);
    posSlopeError = fminbnd(fun, slope, (slope*1.5));
    
    
    f = @(slope, x, xvals, yvals, weights)abs(target-sum(weights.*((yvals-((xvals.*slope)+x)).^2)));
    fun = @(x)f(slope, x, xvals, yvals, weights);
    
    negIntError = fminbnd(fun, -1, intercept);
    posIntError = fminbnd(fun, intercept, 1);
    
    f = @(slope, intercept, xvals, yvals, weights)sum(weights.*((yvals-((xvals.*slope)+intercept)).^2));
    fun = @(slope, intercept)f(slope, intercept, xvals, yvals, weights);
    
    slope_range = [negSlopeError posSlopeError];
    int_range = [negIntError posIntError];
    
    negIntError = intercept - negIntError;
    posIntError = posIntError - intercept;
    
    twoParamOutput.(strcat(id, '_intercept_neg_error')) = negIntError;
    twoParamOutput.(strcat(id, '_intercept_pos_error')) = posIntError;
    
    negSlopeError = slope - negSlopeError;
    posSlopeError = posSlopeError - slope;
    
    twoParamOutput.(strcat(id, '_slope_neg_error')) = negSlopeError;
    twoParamOutput.(strcat(id, '_slope_pos_error')) = posSlopeError;
    
    complete = false;
    while(~complete)
        slope_evals = linspace(slope_range(1), slope_range(2));
        int_evals = linspace(int_range(1), int_range(2));
    
        [slope_grid, int_grid] = meshgrid(slope_evals, int_evals);
    
        chi_grid = cellfun(fun, num2cell(slope_grid), num2cell(int_grid));
        
        [slope_range,int_range,complete] = checkGrid(chi_grid,slope_range, ...
            int_range,(twoParamChi+4));
    end
    
    figure(twoParamChiGraph);
    
    ax = axes('Parent', twoParamChiGraph);
    h = surf(slope_grid, int_grid, chi_grid, 'Parent', ax,...
        'edgecolor', 'none');
    
    hold on;
    
    contour3(slope_grid, int_grid, chi_grid, ...
        [(twoParamChi +1) (twoParamChi +1)], ...
        'ShowText', 'off', 'LineColor', 'w', 'LineWidth', 1.2, ...
        'HandleVisibility', 'off');
    
    view(ax, [0, 90]);
    colormap(parula);
    
    chisqtext = "\chi^{2}"; 
    
    ccb = colorbar;
    ccb.Label.String = chisqtext;
    ccb.Label.FontSize = 12;
    ccb.Label.Rotation = 0;
    pos = get(ccb.Label, 'Position');
    ccb.Label.Position = [pos(1)*1.3 pos(2) 0];
    
    xlabel("Slope");
    ylabel("Intercept");
    txt = "%s vs. Slope and Intercept Parameters";
    title(sprintf(txt, chisqtext));
    
    xlim(slope_range);
    ylim(int_range);


end
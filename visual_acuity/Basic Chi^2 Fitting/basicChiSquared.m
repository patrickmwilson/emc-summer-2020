
experimentName = 'Isolated Character';
subjectName = 'BRADEN';

data = readCsv(experimentName, subjectName, 'both');

data(:,2) = data(:,2).*data(:,1);

twoParameterGraph = figure();

% Set the discreteCol to your x-vals column (retinal eccentricity)
avgData = averageData(data, 1);

avgData = calculateStandardErrors(experimentName, 1, avgData);

xvals = avgData(:,1)';
yvals = avgData(:,2)';
sErrors = avgData(:,4)';

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

twoParamChi = fun(params);

twoParamReducedChi = twoParamChi/(length(xvals)-2);
disp(twoParamReducedChi);

pointSlope(avgData, slope, intercept, 'k', experimentName, ...
    twoParameterGraph);

f = @(x, xvals, yvals, weights)sum((weights.*((yvals-(xvals.*x))).^2));
fun = @(x)f(x, xvals, yvals, weights);

[slope, oneParamChi] = fminbnd(fun, 0, 1);

oneParamReducedChi = oneParamChi/(length(xvals)-1);
disp(oneParamReducedChi);

oneParameterGraph = figure();

pointSlope(avgData, slope, 0, 'k', experimentName, ...
    oneParameterGraph);











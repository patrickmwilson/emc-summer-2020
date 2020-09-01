

close all;
clear variables;

subjectName = 'BRIAN_TA';

folder = fullfile(pwd, 'Plots', subjectName);
mkdir(folder);

info_csv = fullfile(pwd, 'protocol_info.csv');
protocolInfo = table2struct(readtable(info_csv));

oneParamTemplate = fullfile(pwd, 'one_param_struct.csv');
twoParamTemplate = fullfile(pwd, 'two_param_struct.csv');

oneParamOutput = table2struct(readtable(oneParamTemplate));
twoParamOutput = table2struct(readtable(twoParamTemplate));

oneParamOutput.name = subjectName;
twoParamOutput.name = subjectName;

oneParamGraph = figure();
twoParamGraph = figure();

for i=1:length(protocolInfo)
    color = str2num(protocolInfo(i).color);
    experimentName = protocolInfo(i).protocolName;
    discreteCol = protocolInfo(i).discreteCol;
    id = protocolInfo(i).id;

    data = readCsv(experimentName, subjectName, 'both');
    
    if(isempty(data))
        continue;
    end

    data(:,2) = data(:,2).*data(:,1);

    oneParamChiGraph = figure();
    twoParamChiGraph = figure();

    % Set the discreteCol to your x-vals column (retinal eccentricity)
    avgData = averageData(data, discreteCol);

    avgData = calculateStandardErrors(experimentName, discreteCol, avgData);

    oneParamOutput = oneParamChiSquared(avgData, experimentName, id, color, ...
        oneParamGraph, oneParamChiGraph, oneParamOutput);

    twoParamOutput = twoParamChiSquared(avgData, experimentName, id, color, twoParamGraph, ...
        twoParamChiGraph, twoParamOutput);
    
    saveas(oneParamChiGraph, ...
        fullfile(folder, strcat(experimentName, '_one_param_chi_sq.png')));
    
    saveas(twoParamChiGraph, ...
        fullfile(folder, strcat(experimentName, '_two_param_chi_sq.png')));

end


saveas(oneParamGraph, fullfile(folder, 'one_parameter_graph.png'));

saveas(twoParamGraph, fullfile(folder, 'two_parameter_graph.png'));

paramFolder = fullfile(pwd, 'Parameters');
mkdir(paramFolder);



oneParam = struct2table(oneParamOutput);
fileName = fullfile(pwd, 'Parameters', 'one_parameter_statistics.csv');

if(exist(fileName, 'file') ~= 2)
    writetable(oneParam, fileName, 'WriteRowNames', true);
else
    writetable(oneParam, fileName, 'WriteRowNames', false, ...
        'WriteMode', 'Append');
end

twoParam = struct2table(twoParamOutput);
fileName = fullfile(pwd, 'Parameters', 'two_parameter_statistics.csv');

if(exist(fileName, 'file') ~= 2)
    writetable(twoParam, fileName, 'WriteRowNames', true);
else
    writetable(twoParam, fileName, 'WriteRowNames', false, ...
        'WriteMode', 'Append');
end




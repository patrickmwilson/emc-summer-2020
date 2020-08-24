% readCSV
%
% Extracts data from csv files. Normalizes the eccentricity values by
% retinal eccentricity and recursively removes outliers greater than +/-
% 2.5 sigma from the mean of the normalized distribution. Accepts the
% csvName, csvId, data type, subject name, and a boolean indicating whether
% to remove small eccentricity values from crowded center as input
% arguments. Returns the raw data, truncated data, and any outliers.
function [rawData,data,outliers] = readCsv(experimentName,subjectName,direction)
    
    % Suppress warning about modified csv headers
    warning('off','MATLAB:table:ModifiedAndSavedVarnames');
    
    % Creates filepaths to all the subfolders within each base folder
    folderPaths = [];

    baseFolder = string(fullfile(pwd, 'Data'));

    folders = dir(baseFolder);
    folderNames={folders(:).name}';
    for j=1:size(folderNames,1)
        folderName = string(folderNames{j,1});

        if(startsWith(folderName,"."))
            continue; % Skips folders such as .DS_STORE
        end

        % If a subject was specified, skip any folders which do not
        % match the subject code
        if(~strcmp(subjectName,'All'))
            if(~strcmp(subjectName,folderName))
                continue;
            end
        end

        % Create the new file path and append it to the array
        folderPath = string(fullfile(baseFolder, folderName));
        folderPaths = [folderPaths folderPath];  
    end

    rawData = []; data = []; outliers = [];
    for i=1:length(folderPaths)
        folder = folderPaths(i);
        
        % Get the names of all the csv files within the folder
        files = dir(folder);
        fileNames={files(:).name}';
        csvFiles=fileNames(endsWith(fileNames,'.csv'));
        
        % Loop over every csv file, extracting data from files which match
        % the search conditions
        for j=1:size(csvFiles,1)
            file = char(csvFiles{j,1});
            
            % csv file names follow this convention:
            % SUBJECT_DATE_PROTOCOLNAME.csv
            underscores = find(file == '_'); % Find indices of underscores
            period = find(file == '.'); % Find the period

            % Extract the portion of the csv file name between the last
            % underscore and the period
            protocolName = string(extractBetween(file, (underscores(end)+1), (period-1)));
            if(~strcmp(protocolName, experimentName))
                continue; % Skip csv files from other protocols
            end
            
            thisData = []; thisFitData = []; theseOutliers = [];
            
            % Extract the data from the csv into an array
            filename = fullfile(folder, string(csvFiles(j,1)));
            raw = table2array(readtable(filename));
        
            % Creates a 3 column matrix of the data. Eccentricity is placed in
            % col 1, letter height in col 2, direction in col 3
            thisData(:,1) = raw(:,3);
            % T1 data is stored differently, letter height is in column 4 of
            % the csv rather than column 2
            thisData(:,2) = raw(:,2);
            thisData(:,3) = raw(:,1);
            
            % Sets the eccentricity values which are to be excluded from
            % the data
            exclusions = [0];
            
            % Set directions to include in the data based on the dir input
            % argument. 
            if(strcmp(direction,'both'))
                dirs = [1,3];    
            elseif(strcmp(direction,'right'))
                dirs = [1];
            else
                dirs = [3];
            end

            % Removes all rows from the data matrix which contain a zero,
            % contain an eccentricity value that is included in the
            % exclusions array, or do not match the specified direction
            k = 1;
            while(k <= size(thisData,1))
                if(ismember(thisData(k, 1), exclusions) || thisData(k,2) == 0)
                    thisData(k,:) = [];
                    continue;
                elseif(~ismember(thisData(k,3),dirs))
                    thisData(k,:) = [];
                    continue;
                end
                k = k + 1;
            end
            
            % Remove the direction information as it is no longer needed
            thisData(:,3) = [];

            % Normalize letter height observations by retinal eccentricity 
            thisData(:,2) = thisData(:,2)./thisData(:,1);
    
            % Recursively removing outliers more than 2.5 standard 
            % deviations (99% confidence interval) from the normalized 
            % distribution (see removeOutliers.m)
            [thisFitData,theseOutliers] = removeOutliers(thisData, [], ...
                2.5, 2);

            % Concatenate these values with accumulated values
            rawData = [rawData; thisData];
            data = [data; thisFitData];
            outliers = [outliers; theseOutliers];
        end
    end
end
% removeOutliers
%
% Recursively truncates a distribution, removing any value greater than 
% +/- the specified sigma value from the mean. Accepts a matrix, a cutoff 
% sigma, and the column of interest as input. Recursively computes the 
% Z-score of the column of interest and removes row elements that have a 
% Z-score higher than the cutoff. 
function [newData,outliers] = removeOutliers(data, outliers, cutOff, columnOfInterest)
    
    % Compute Z-score of the column of interest and store it in a new
    % column
    newData = data;
    z = zscore(newData(:,columnOfInterest));
    newData(:,(size(data,2)+1)) = z(:,1);
    
    % Remove any rows which contain a Z-score higher than the cutoff
    i = 1;
    while(i <= size(newData,1))
        if(abs(newData(i,(size(data,2)+1))) > cutOff)
            outliers = [outliers; newData(i,:)];
            newData(i,:) = [];
            continue;
        end
        i = i+1;
    end
    
    % Remove the column storing the Z-scores
    newData(:,(size(data,2)+1)) = [];
    
    % If any elements were removed, remove outliers from the remaining
    % elements
    if(size(newData,1) ~= size(data,1))
        [newData,outliers] = removeOutliers(newData, outliers, cutOff, columnOfInterest);
    end
    
end

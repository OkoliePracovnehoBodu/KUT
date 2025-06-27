clear all;
clc;


inputSigRange = [0, 10];

inputPointsNo = 11;

steadyTime = 60; 




inputPoints = linspace(inputSigRange(1), inputSigRange(2), inputPointsNo);

inputTable = [];

for rowidx = 1:length(inputPoints)

    inputTable(rowidx,:) = [  steadyTime * (rowidx-1), inputPoints(rowidx)];

end

simStopTime = steadyTime * rowidx



writematrix(inputTable, "./dataRepo/" + "tmp_inputTable_" + string(datetime('now','Format','yyyy-MM-dd_HH_mm_ss')) + ".csv")

load('demo.mat')

% Combine variables into a matrix (each as a column)
data = [t, vent, spir, snim1, snim2];

% Save to CSV file
csvwrite('demo.csv', data);
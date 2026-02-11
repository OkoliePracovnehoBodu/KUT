

% Assuming there is Dataset logsout



figure(101);



subplot(3,1,1)

plot(logsout{1}.Values.Time, logsout{1}.Values.Data, '.')

title(replace(logsout{1}.Values.Name,"_"," "))



subplot(3,1,2)

plot(logsout{2}.Values.Time, logsout{2}.Values.Data, '.')

title(replace(logsout{2}.Values.Name,"_"," "))



subplot(3,1,3)

plot(logsout{3}.Values.Time, logsout{3}.Values.Data, '.')

title(replace(logsout{3}.Values.Name,"_"," "))







% BTW this is also possible:
plot(logsout)


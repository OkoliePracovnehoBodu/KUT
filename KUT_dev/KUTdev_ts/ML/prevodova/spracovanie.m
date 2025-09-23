clc
clear
close all

load prevodova_vent6.mat

time = time(1:end-1);
snimac1 = snimac1(1:end-1);
snimac2 = snimac2(1:end-1);
spir = spir(1:end-1);
vent = vent(1:end-1);

for i = 1:11
    from = (i-1)*1000 + 899;
    to = from + 100;
    static1(i) = mean(snimac1(from:to));
    static2(i) = mean(snimac2(from:to));
    in(i) = i-1;
end

csvwrite('prevodova6.csv', [time, vent, spir, snimac1, snimac2]);
csvwrite('static6.csv', [in', static1', static2']);

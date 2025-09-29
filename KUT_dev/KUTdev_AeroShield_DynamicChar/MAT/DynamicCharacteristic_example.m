format short;
close all;

% ----------------------------------
% Create data directory if not created
% ----------------------------------

DDIR = "dataRepo";
if ~exist(DDIR, "dir")
    fprintf("Creating the data directory...");
    mkdir(DDIR);
end

% ----------------------------------
% ----------------------------------



% ----------------------------------
% Open File Stream
% ----------------------------------

DateString = convertCharsToStrings(datestr(datetime('now'), "yyyy_mm_dd_HH_MM_ss"));

datafileID = fopen("./" + DDIR + "/" + "dataFile_" + DateString + ".csv",'w');
fprintf(datafileID, 't,tp,r,y,u,dt_plant,dt\n');

% ----------------------------------
% ----------------------------------


% ----------------------------------
% Define simulation parameters
% ----------------------------------

T_start = 0;

T_sample = 0.06;      % [sec]

STEP_SIZE = 5; % [%PWM]

U_PB = 20; % [%PWM] pracovny bod, OP - operating point

T_step_time = 15; % [sec]

STEP_SHAPE = [1, 0, -1, 0, 1, -1, 1, 0]; % step up, down, down, up, up, large down, large up, down

nsteps = length(STEP_SHAPE);

T_stabilize_time = 30; % [sec] Cas stabilizacie v PB

% Define control parameters

U_MAX = 100.0;
U_MIN = 0.0;
Y_SAFETY = 100.0;

% Define STOP TIME

T_stop = T_stabilize_time + T_step_time * nsteps;  % [sec]

% Define U increments to get to the U_PB smoothly
dU = ceil(U_PB/T_stabilize_time*10)/10;


fprintf(2, "Simulation will be running for the next: %8.3f seconds, with %8.3f steps\n", T_stop, nsteps + 1);

% ----------------------------------
% ----------------------------------



% ----------------------------------
% Initiate Plot Figure
% ----------------------------------

plot_window = 20;
plot_idx_num = floor(plot_window/T_sample);
 
plot_t = nan(plot_idx_num,1);
plot_sig_1 = nan(plot_idx_num,1);
plot_sig_2 = nan(plot_idx_num,1);
plot_sig_3 = nan(plot_idx_num,1);

figure(666);
clf;

% ----------------------------------
% ----------------------------------



% ----------------------------------
% Record measurement data
% ----------------------------------


function updateInfo(datafileID, dt, Ts, x)
    if ((dt/1000) > (Ts*1.05))
        fprintf('%8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f --\n', x);
    else
        fprintf('%8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f\n', x);
    end
    fprintf(datafileID, '%8.3f,%8.3f,%8.3f,%8.3f,%8.3f,%8.3f,%8.3f\n', x);
end

doUpdate = @(x) updateInfo(datafileID, x(end), T_sample, x);

% ----------------------------------
% ----------------------------------


% ----------------------------------
% Setup connection with the Arduino UNO R3 device using Serial Link
% ----------------------------------

% Define serial port parameters and open
serPort = serialport('COM3', 115200, 'Timeout', 5);

% Read the first line from the serial port
serLine = readline(serPort);
disp(serLine);

% write(serPort, 0.0, 'single');

% Read and parse the calibration data
serLineList = str2num(readline(serPort)); %#ok<ST2NM>

% Extract values from the received data
plant_time_init = serLineList(1);
plant_potentiometer_init = serLineList(2);
plant_output_init = serLineList(3);
plant_input_init = serLineList(4);

plant_time = serLineList(1) - plant_time_init;
plant_potentiometer = 60; %serLineList(2);
plant_output = serLineList(3);
plant_input = serLineList(4);
plant_dt = serLineList(5);

% Display and record the received data
tmp_printlist = [0, plant_time, plant_potentiometer, plant_output, plant_input, plant_dt/1000, T_sample * 1000];
doUpdate(tmp_printlist);

% ----------------------------------
% ----------------------------------


% ----------------------------------
% Setup loop variables
% ----------------------------------

% Set initial control input value
u = 0;
u_send = u;

istep = 1; % Holding the step index within the STEP_SHAPE matrix
wasstepchange = false; % Check whether a change in step happened within the iteration
isstable = false;

% Get the initial time
time_start = datetime('now');
time_tick = time_start;
time_step = time_start;
time_stabilize = time_start;

% ----------------------------------
% ----------------------------------


% ----------------------------------
% Main loop
% ----------------------------------
while true
    % Get current time
    time_curr = datetime('now');
    
    % Calculate time elapsed since last iteration
    time_delta = milliseconds(time_curr - time_tick);

    % ----------------------------------
    % Logic behind the measurement, before sending the data
    % ----------------------------------
    
    if (~isstable && milliseconds(time_curr - time_stabilize)/1000 >= T_stabilize_time)
        isstable = true;
    end

    if (isstable && milliseconds(time_curr - time_step)/1000 >= T_step_time)
        time_step = time_curr;
        u = U_PB + STEP_SHAPE(istep) * STEP_SIZE;
        istep = istep + 1;
        wasstepchange = true;
    end

    % ----------------------------------
    % ----------------------------------

    
    % ----------------------------------
    % Receiving and Sending data
    % ----------------------------------

    % Check if it's time to send a new command
    if (wasstepchange || time_delta >= T_sample * 1000)
        wasstepchange = false; % Reset the step change variable, to keep to the defined sampling period
        time_tick = time_curr;
        
        % Calculate total time elapsed
        time_elapsed = seconds(time_curr - time_start);

        % Send control input to the serial port
        write(serPort, u_send, 'single');
        
        % Read and parse the received data
        serLineList = str2num(readline(serPort)); %#ok<ST2NM>
        
        % Extract values from the received data
        plant_time = serLineList(1) - plant_time_init;
        plant_potentiometer = 60; %serLineList(2)/100*90; % Scale the potentiometer output to 0 - 90 degrees
        plant_output = serLineList(3);
        plant_input = serLineList(4);
        plant_dt = serLineList(5);
        
        % Display the received data
        tmp_printlist = [time_elapsed, plant_time, plant_potentiometer, plant_output, plant_input, plant_dt/1000, time_delta];

        doUpdate(tmp_printlist);

        % ----------------------------------
        % Plot the measured data in real time
        % ----------------------------------
        
        plot_t = circshift(plot_t, -1);
        plot_t(end) = time_elapsed;

        plot_sig_1 = circshift(plot_sig_1, -1);
        plot_sig_1(end) = plant_output;

        plot_sig_2 = circshift(plot_sig_2, -1);
        plot_sig_2(end) = plant_potentiometer;

        plot_sig_3 = circshift(plot_sig_3, -1);
        plot_sig_3(end) = plant_input;

        plot(plot_t, plot_sig_3,'.b', plot_t, plot_sig_2,'.r', plot_t, plot_sig_1,'.k' )
        xlim([min(plot_t), max(plot_t)+T_sample])
        ylim([min(plot_sig_1) - 5, max(plot_sig_1) + 5]);
        grid on;
        legend("u","ref","y");

        drawnow nocallbacks

        % ----------------------------------
        % ----------------------------------

        % ----------------------------------
        % Calcualte 'u' - control output (akcny zasah)
        % ----------------------------------
        if(~isstable && u < U_PB)
            u = min(u + dU, U_PB);
        end

        u_send = u;
        
        if u_send > U_MAX
            u_send = U_MAX;
        elseif u_send < U_MIN
            u_send = U_MIN;
        end  

        % ----------------------------------
        % ----------------------------------

        
        % ----------------------------------
        % End loop condition - check if the simulation should stop
        % ----------------------------------
        
        if time_elapsed >= T_stop || plant_output >= Y_SAFETY 
            break;
        end

        % ----------------------------------
        % ----------------------------------
    end
    % ----------------------------------
    % ----------------------------------
end



% ----------------------------------
% Close Serial Comms and File Stream
% ----------------------------------

% Send a final command and close the serial port
write(serPort, 0.0, 'single');
clear serPort;
fclose(datafileID);

% ----------------------------------
% ----------------------------------

% ----------------------------------
% Save the data into a MAT file for further analysis
% ----------------------------------

logsout = readtable("./" + DDIR + "/" + "dataFile_" + DateString + ".csv", "VariableNamingRule","preserve","Delimiter",",");

save("./" + DDIR + "/" + "dataFile_" + DateString, "U_MAX", "U_MIN", "Y_SAFETY", "T_sample", "T_start", "T_stop", "T_stabilize_time", "T_step_time", "U_PB", "dU", "STEP_SHAPE", "STEP_SIZE", "u", "logsout");

% ----------------------------------
% ----------------------------------

% ----------------------------------
%% Plot the recorded data
% ----------------------------------

t = logsout.t;
y = logsout.y;
u = logsout.u;
r = logsout.r;
e = r - y;
dt = logsout.dt;


figure(111);
hold on;
plot(t, y, '-k', 'LineWidth', 1.5);
plot(t, u, '--b', 'LineWidth', 1.5);
title('Control Response');
legend('y(t)', 'u(t)', "Location", "best");
xlim([0, max(t) + T_sample]);
if min(y) ~= max(y)
    ylim([min(y), max(y)]);
end
xlabel('t [s]');
ylabel('value [deg]/[%]');
grid on;
hold off;

% ----------------------------------
% ----------------------------------
format short;

function [timer_t, timer_y, timer_u, timer_potentiometer, timer_yhat, timer_dyhat] = runArduinoPlot()
    % ----------------------------------
    % Create the data repository
    % ----------------------------------
    DDIR = "dataRepo";
    if ~exist(DDIR, "dir")
        fprintf("Creating the data directory...");
        mkdir(DDIR);
    end
    % ----------------------------------
    % ----------------------------------

    % ----------------------------------
    % Define all the parameters
    % ----------------------------------
    
    % Define time parameters
    
    T_start = 0;
    
    T_sample = 3;      % [ms] <1, 255>
    
    % Define STOP TIME
    
    T_stop = 60.0;     % [sec]
    
    % Define control parameters
    U_MAX = 100.0;
    U_MIN = 0.0;
    Y_SAFETY = 190.0;
    
    % Define PID param
    P = 1.0;
    I = 0.30;
    D = 0.19;
    
    R_WANTED = 140;

    % alpha - beta filter
    alpha = 0.8;
    beta = 0.2;

    timer_t = [];
    timer_y = [];
    timer_yhat = [];
    timer_dyhat = [];
    timer_u = [];
    timer_potentiometer = [];
    % ----------------------------------
    % ----------------------------------
    
    

    % ----------------------------------
    % Plot the measured data in real time
    % ----------------------------------
    function plotData()
        persistent hy hr hu;
        try
            if isempty(hy) || isempty(hr) || isempty(hu)
                f = figure(9999); clf(f);
                ax = axes(f);
                hold on;
                hy = plot(ax, nan, nan, '.b');
                hr = plot(ax, nan, nan, '.r');
                hu = plot(ax, nan, nan, '.k');
                grid minor;
                title("Real-Time System Response");
                xlabel("t [s]");
                ylabel("$\varphi [^\circ]$", "Interpreter","latex");
                legend(ax, "y","ref", "yhat", 'Location', 'southeast');
                
            end
           
            % plot(plot_t, plot_sig_3,'.b', plot_t, plot_sig_2,'.r', plot_t,
            % plot_sig_1,'.k')
            % print(timer_t(1));

            set(hy, 'YData', timer_y, 'XData', timer_t);
            set(hr, 'YData', timer_potentiometer, 'XData', timer_t);
            set(hu, 'YData', timer_yhat, 'XData', timer_t);
            drawnow limitrate nocallbacks;
        catch err
           fprintf(2, "Plot thread: " + err.message + "\n");
        end
    end
    
    tPlot = timer('ExecutionMode','fixedRate', 'Period', 0.5, 'TimerFcn', @(~, ~) plotData());
    start(tPlot);
    % ----------------------------------
    % ----------------------------------

    % ----------------------------------
    % Initialize File Streams
    % ----------------------------------
    
    DateString = convertCharsToStrings(datestr(datetime('now'), "yyyy_mm_dd_HH_MM_ss"));
    
    FILENAME = "dataFile";
    
    function fullpath = getfilename(dirpath, filename, datestr, ext)
        if nargin < 3
            error("At least the first 3 parameters need to be provided.");
        end
        if nargin == 3
            ext = "csv";
        end
    
        fullpath = "./" + dirpath + "/" + filename + "_" + datestr + "." + ext;
    end
    
    FILEPATH = getfilename(DDIR, FILENAME, DateString);
    FILEPATH_MAT = getfilename(DDIR, FILENAME, DateString, 'mat');
    
    if(exist("datafileID", "var"))
        fclose(datafileID);
        clear datafileID;
    end
    
    datafileID = fopen(FILEPATH,'w');
    fprintf(datafileID, 't, tp, r, y, u, dtp, dt\n');
    % ----------------------------------
    % ----------------------------------
    
    % ----------------------------------
    % Write data into files
    % ----------------------------------
    
    function updateInfo(datafileID, dt, Ts, x)
        if ((dt) > (Ts*1.05))
            fprintf('%8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f  --\n', x);
        else
            fprintf('%8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f\n', x);
        end
        fprintf(datafileID, '%8.3f, %8.3f, %8.3f, %8.3f, %8.3f, %8.3f, %8.3f\n', x);
        timer_t = [timer_t x(1)];
        timer_y = [timer_y x(4)];
        timer_u = [timer_u x(5)];
        timer_potentiometer = [timer_potentiometer x(3)];
    end
    
    doUpdate = @(x) updateInfo(datafileID, x(end), T_sample, x);
    
    % ----------------------------------
    % ----------------------------------

    % ----------------------------------
    % Define serial port parameters, open and configure comms
    % ----------------------------------
    
    if(exist("serPort", "var"))
        serPort.flush("input");
        clear serPort;
    end
    
    serPort = serialport('COM3', 115200, 'Timeout', 5);
    
    serLine = readline(serPort);
    
    while(~contains(serLine, "config"))
        disp(serLine);
        serLine = readline(serPort);
    end
    
    fprintf("Sending now\n");
    write(serPort, cast(T_sample, "uint8"), "uint8");
    
    % Read the first line from the serial port (MCU starting)
    while(~contains(serLine, "start"))
        disp(serLine);
        serLine = readline(serPort);
    end
    
    disp(serLine);
    write(serPort, 0.0, 'single'); % Necessary to send this command for stable sampling period
    
    while(contains(serLine, "---"))
        disp(serLine);
        serLine = readline(serPort);
    end
    
    % Read and parse the calibration data
    serLineList = str2num(serLine); %#ok<ST2NM>

    % ----------------------------------
    % ----------------------------------

    % ----------------------------------
    % Extract the initial values from the received data
    % ----------------------------------
    plant_time_init = serLineList(1);
    plant_potentiometer_init = serLineList(2);
    plant_output_init = serLineList(3);
    plant_input_init = serLineList(4);
    
    plant_time = serLineList(1) - plant_time_init;
    plant_input = serLineList(2);
    plant_output = serLineList(3);
    plant_potentiometer = R_WANTED + serLineList(4)/100*20;
    plant_dt = serLineList(5);

    timer_yhat = [timer_yhat, plant_output];
    timer_dyhat = [timer_dyhat, 0];
    
    % Display the received data
    tmp_printlist = [0, plant_time, plant_potentiometer, plant_output, plant_input, plant_dt, T_sample];
    doUpdate(tmp_printlist);
    % ----------------------------------
    % ----------------------------------

    % ----------------------------------
    % Set the main loop parameters
    % ----------------------------------
    
    % Set initial control input value
    e_old = 0;
    e_int_old = 0;
    u = 0;
    u_send = u;
    
    
    % Get the initial time
    time_start = datetime('now');
    time_tick = time_start;

    % ----------------------------------
    % ----------------------------------
    

    % ----------------------------------
    % Define serial link listener
    % ----------------------------------
    
    function readSerialData(src, ~) 
        data = readline(src);
        src.UserData = data;
    end
    
    configureCallback(serPort, "terminator", @readSerialData);
    % ----------------------------------
    % ----------------------------------
    
    
    % ----------------------------------
    % Main loop
    % ----------------------------------
    while true
        % ----------------------------------
        % Process the read data from the serial communication
        % ----------------------------------
        waitfor(serPort, "UserData");

        % Get current time
        time_curr = datetime('now');
    
        % Calculate time elapsed since last iteration
        time_delta = milliseconds(time_curr - time_tick);
    
        % Read and parse the received data
        serLineList = str2num(serPort.UserData); %#ok<ST2NM>
    
        time_tick = time_curr;
    
        % Calculate total time elapsed
        time_elapsed = seconds(time_curr - time_start);
    
        % Extract values from the received data
        plant_time = serLineList(1) - plant_time_init;
        plant_input = serLineList(2);
        plant_output = serLineList(3);
        plant_potentiometer = R_WANTED + serLineList(4)/100*20;
        plant_dt = serLineList(5);
        
        dx = plant_output - timer_yhat(end);
        cyhat = timer_yhat(end) + alpha*(dx);
        timer_yhat = [timer_yhat, cyhat];
        timer_dyhat = [timer_dyhat, timer_dyhat(end) + beta*(dx/time_delta)];
    
        % Record the received data
        tmp_printlist = [time_elapsed, plant_time, plant_potentiometer, plant_output, plant_input, plant_dt, time_delta];
        doUpdate(tmp_printlist);

        % ----------------------------------
        % ----------------------------------
    
        % ----------------------------------
        % Insert your code here (for example, we have PID controller code implemented in this space)
        % ----------------------------------
    
        e = plant_potentiometer - plant_output;
    
        e_der = (e - e_old) / (time_delta/1000);
    
        e_int = e_int_old + (e * (time_delta/1000));
    
        e_old = e;
        e_int_old = e_int;
    
    
        u = P * e  +  I * e_int + D * e_der;

        % ----------------------------------
        % ----------------------------------

        % ----------------------------------
        % Saturate the control output to the MAX and MIN values
        % ----------------------------------
    
        u_send = u;
    
        if u_send > U_MAX
            u_send = U_MAX;
        elseif u_send < U_MIN
            u_send = U_MIN;
        end

        % ----------------------------------
        % ----------------------------------

        % ----------------------------------
        % Send control input to the serial port
        % ----------------------------------
    
        write(serPort, u_send, "single");
    
        % ----------------------------------
        % ----------------------------------

        % ----------------------------------
        % Check if the simulation should stop (safety precaution)
        % ----------------------------------
    
        if time_elapsed >= T_stop || plant_output >= Y_SAFETY
            configureCallback(serPort, "off"); % Remove the callback from the serial port, before exiting the loop
            break;
        end

        % ----------------------------------
        % ----------------------------------
    end

    % ----------------------------------
    % ----------------------------------

    % ----------------------------------
    % Close and delete all the existing timers
    % ----------------------------------
    
    for tim=timerfindall
        stop(tim);
        delete(tim);
    end

    % ----------------------------------
    % ----------------------------------

    % ----------------------------------
    % Close the serial connection
    % ----------------------------------

    % Send a final command and close the serial port
    write(serPort, 0.0, 'single');
    serPort.flush("input");
    clear serPort;
    fclose(datafileID);
    clear datafileID;

    % ----------------------------------
    % ----------------------------------

    % ----------------------------------
    % Save the measurement into a .MAT file for easier access to data when using Matlab
    % ----------------------------------

    logsout = readtable(FILEPATH, "VariableNamingRule","preserve","Delimiter",",");

    save(FILEPATH_MAT);

    % ----------------------------------
    % ----------------------------------

    % ----------------------------------
    % Quickly plot the measurement - reference, output, and control signal
    % ----------------------------------
    
    t = logsout.t;
    y = logsout.y;
    u = logsout.u;
    r = logsout.r;
    e = r - y;
    dt = logsout.dtp;
    
    
    figure(111);
    hold on;
    plot(t, y, '-k', 'LineWidth', 1.5);
    plot(t, r, '-r', 'LineWidth', 1.5);
    plot(t, u, '-b', 'LineWidth', 1.5);
    title('Control Response');
    subtitle("P = " + num2str(P) + ", I = " + num2str(I) + ", D = " + num2str(D));
    legend('y(t)', 'ref(t)', 'u(t)', "Location", "best");
    xlabel('t [s]');
    ylabel('y [deg]');
    grid on;
    hold off;
    % ----------------------------------
    % ----------------------------------

end
% ----------------------------------
% ----------------------------------

% ----------------------------------
% Run the experiment using the following line of code
% ----------------------------------

[t, y, u, potentiometer, yhat, dyhat] = runArduinoPlot();

% ----------------------------------
% ----------------------------------

% ----------------------------------
%% Plot the data
% ----------------------------------

figure(100);
subplot(3, 1, 1);
plot(t, y, t, yhat, t, potentiometer, 'LineWidth', 1.5);
grid minor;
legend('y','yhat','ref');
xlabel('t [s]');
ylabel('$\varphi [^\circ]$', 'Interpreter', 'latex');
title('System response');
subtitle("$\alpha - \beta$ filter", 'Interpreter', 'latex');

subplot(3, 1, 2);
plot(t, dyhat, 'LineWidth', 1.5);
grid minor;
xlabel('t [s]');
ylabel('$\omega [^\circ/s]$', 'Interpreter', 'latex');
title('System velocity response');
subtitle("$\alpha - \beta$ filter", 'Interpreter', 'latex');

subplot(3, 1, 3);
plot(t, (y-yhat), 'LineWidth', 1.5);
grid minor;
xlabel('t [s]');
ylabel('$\varphi [^\circ]$', 'Interpreter', 'latex');
title('Observer error');
subtitle("$\alpha - \beta$ filter", 'Interpreter', 'latex');

% ----------------------------------
% ----------------------------------
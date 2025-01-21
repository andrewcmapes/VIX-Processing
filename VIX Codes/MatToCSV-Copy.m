clear;

p = 'https://cdn.cboe.com/data/us/futures/market_statistics/historical_data/VX/';

for year = 2014:2024
    for month = 1:12
        for day = 1:31
            if month < 10
                m = ['0' num2str(month)];
            else
                m = num2str(month);
            end
            if day < 10
                d = ['0' num2str(day)];
            else
                d = num2str(day);
            end

            fn = ['VX_' num2str(year) '-' m '-' d];

            url = [p fn '.csv'];
            tic
            data = [];
            fno = [num2str(year) m d '.mat'];
            try
                data = webread(url);
            end

            if ~isempty(data)
                % Convert data to table format if it's not already in table format
                if ~istable(data)
                    data = struct2table(data);
                end
                
                % Generate CSV filename
                csvFilename = fullfile(pwd, [fn '.csv']);
                
                % Write table data to CSV file
                writetable(data, csvFilename);
                disp(['Converted ' fn '.csv']);
            end
        end
    end
end

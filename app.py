def save_logs_to_csv():
    if os.path.exists('email_opens.log'):
        print("email_opens.log exists")
        # Read the log file
        with open('email_opens.log', 'r') as f:
            lines = f.readlines()
        
        # Parse log lines
        data = []
        for line in lines:
            parts = line.strip().split(' - ')
            if len(parts) == 2:
                timestamp, message = parts
                if ' - ATECO: ' in message:
                    email = message.split(': ')[1].split(' - ATECO: ')[0]
                    ateco = message.split(' - ATECO: ')[1]
                    data.append([timestamp, email, ateco])
                else:
                    print(f"Skipping malformed line: {line.strip()}")
                    logging.warning(f"Skipping malformed line: {line.strip()}")
            else:
                print(f"Skipping malformed line: {line.strip()}")
                logging.warning(f"Skipping malformed line: {line.strip()}")
        
        # Create a DataFrame and save to CSV
        if data:  # Only save if there's data
            df = pd.DataFrame(data, columns=['Timestamp', 'Email', 'ATECO'])
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv_filename = f'email_opens_{timestamp}.csv'
            df.to_csv(csv_filename, index=False)
            print(f"File saved: {csv_filename}")
            logging.info(f"CSV file saved: {csv_filename}")
        else:
            print("No valid data to save to CSV.")
            logging.info("No valid data to save to CSV.")
    else:
        print("email_opens.log does not exist")
        logging.error("email_opens.log does not exist")
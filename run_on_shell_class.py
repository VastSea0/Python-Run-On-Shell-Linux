 def run_on_shell(self):
        # Get sudo password from the user
        sudo_password, ok_pressed = QInputDialog.getText(self, 'Sudo şifresi', 'Sudo şifreni gir:', QLineEdit.Password)

        if ok_pressed:
            # Find the selected program based on the app_id
            with open('apps.json', 'r') as file:
                apps_data = json.load(file)

            selected_program = next((app for app in apps_data if app.get('appId') == self.app_id), None)

            if selected_program:
                app_command = selected_program.get('appCommand', '')
                try:
                    # Execute the command with sudo/root privileges and capture the output
                    command = f'sudo -S {app_command}'
                    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    # Send sudo password
                    process.stdin.write(sudo_password + '\n')
                    process.stdin.flush()

                    # Wait for the subprocess to finish
                    process.wait()

                    # Check if the command asks for user input
                    if "[E/h]" in process.stdout.read():
                        # Prompt the user for input
                        response, ok_pressed = QInputDialog.getItem(self, 'Devam et', 'Bu işlemi devam ettirmek ister misiniz?', ['E', 'h'], 0)

                        # If user wants to continue, send the response to the command
                        if ok_pressed and response == 'E':
                            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            process.stdin.write('E\n')
                            process.stdin.flush()

                    # Open a new dialog to display the terminal output
                    output_dialog = OutputDialog(process.stdout.read(), process.stderr.read())
                    output_dialog.exec_()

                    # Ask the user if they want to close the terminal
                    response = self.ask_to_close_terminal()

                    if response == "Yes":
                        self.close()
                except subprocess.CalledProcessError as e:
                    print(f"Error executing the command: {e}")
                    print(f"Command output (stdout): {e.stdout}")
                    print(f"Command output (stderr): {e.stderr}")






# BU SADECE BİR KULLANIM ÖRNEĞİ README.MD DOSYASINDAN DETAYLICA KODLARI İNCELEYEBİLİRSİNİZ
#HAPPY HACKİNG!!

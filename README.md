# Füze Paket Yükleyicisi Arayüz Sınıfı

Bu Python sınıfı, Linux terminaline arayüz ile komut göndermeye olanak tanır. Genellikle Füze Paket Yükleyicisi yazılımının bir parçasıdır ve diğer yazılımcıların terminale komut göndermelerini kolaylaştırmak için tasarlanmıştır.

## Kullanım

Sınıf, PyQt5 kütüphanesi kullanılarak geliştirilmiştir ve aşağıdaki temel adımları içerir:

1. **Sudo Şifresi Alma**: Kullanıcıdan sudo/root yetkileri için şifre alır.

    ```python
    sudo_password, ok_pressed = QInputDialog.getText(self, 'Sudo Şifresi', 'Sudo şifrenizi girin:', QLineEdit.Password)
    ```

2. **Seçilen Program Bilgisini Alma**: 'apps.json' dosyasındaki verileri kullanarak, kullanıcının seçtiği programa ait bilgileri alır.

    ```python
    with open('apps.json', 'r') as file:
        apps_data = json.load(file)
    selected_program = next((app for app in apps_data if app.get('appId') == self.app_id), None)
    ```

3. **Komutu Sudo Yetkileriyle Çalıştırma**: Sudo yetkileriyle bir komutu çalıştırmak için subprocess kütüphanesini kullanır. Kullanıcıdan alınan sudo şifresini kullanarak işlemi başlatır.

    ```python
    command = f'sudo -S {app_command}'
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    ```

4. **Kullanıcı Girişi Gerekiyorsa İşlemi Tamamlama**: Eğer komut kullanıcı girişi istiyorsa, kullanıcıya bir giriş ile devam etme seçeneği sunar.

    ```python
    if "[E/h]" in process.stdout.read():
        response, ok_pressed = QInputDialog.getItem(self, 'Devam Et', 'Bu işlemi devam ettirmek ister misiniz?', ['E', 'h'], 0)
    ```

5. **Terminal Çıktısını Gösterme**: İşlemin çıktılarını bir yeni pencerede gösterir.

    ```python
    output_dialog = OutputDialog(process.stdout.read(), process.stderr.read())
    output_dialog.exec_()
    ```

6. **Terminali Kapatma İsteği**: Kullanıcıdan terminali kapatmak isteyip istemediğini sorar.

    ```python
    response = self.ask_to_close_terminal()
    if response == "Yes":
        self.close()
    ```

## Hata Durumları

Eğer bir komut çalıştırılırken hata oluşursa, `subprocess.CalledProcessError` yakalanır ve hatayla ilgili bilgiler yazdırılır.

```python
except subprocess.CalledProcessError as e:
    print(f"Komutu çalıştırma hatası: {e}")
    print(f"Komut çıktısı (stdout): {e.stdout}")
    print(f"Komut çıktısı (stderr): {e.stderr}")
```
# Lisans
Bu sınıf açık kaynaklıdır ve MIT Lisansı altında lisanslanmıştır.

Bu README.md dosyası, sınıfınızın temel kullanımını ve hata durumlarını anlamak için diğer geliştiricilere rehberlik etmek üzere tasarlanmıştır. Dilerseniz, belgeleri özelleştirebilir ve daha fazla detay ekleyebilirsiniz.

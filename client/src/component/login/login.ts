import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {
  username: string = '';
  password: string = '';
  rememberMe: boolean = false;
  showPassword: boolean = false;
  isLoading: boolean = false;
  errorMessage: string = '';
  showDemoInfo: boolean = true;
  currentYear: number = new Date().getFullYear();

  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }

  onForgotPassword(event: Event): void {
    event.preventDefault();
    this.errorMessage = '';
    alert('Şifre sıfırlama bağlantısı e-posta adresinize gönderilecektir.');
  }

  onSignup(event: Event): void {
    event.preventDefault();
    this.errorMessage = '';
    alert('Kayıt sayfasına yönlendiriliyorsunuz...');
  }

  onSubmit(form: any): void {
    if (form.invalid) {
      // Tüm alanları touched yaparak hataları göster
      Object.keys(form.controls).forEach(key => {
        form.controls[key].markAsTouched();
      });
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    // Demo giriş kontrolü
    if (this.username === 'demo' && this.password === 'demodemo') {
      setTimeout(() => {
        this.isLoading = false;
        alert(`Giriş başarılı!\nHoş geldiniz, ${this.username}!`);
        // Burada gerçek uygulamada routing yapılır
      }, 1500);
    } else {
      // Simüle edilmiş API çağrısı
      setTimeout(() => {
        this.isLoading = false;
        this.errorMessage = 'Kullanıcı adı veya şifre hatalı. Lütfen tekrar deneyin.';
      }, 1500);
    }
  }
}
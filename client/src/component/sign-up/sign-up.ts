import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sign-up', // Seçicinin HTML ile uyumlu olduğundan emin olun
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './sign-up.html',
  styleUrls: ['./sign-up.css']
})
export class SignUp {
  // HATA ÇÖZÜMÜ: HTML'de 'user.fullName' vb. kullandığınız için bu objeyi tanımlıyoruz
  user = {
    fullName: '',
    username: '',
    email: '',
    password: ''
  };

  // HATA ÇÖZÜMÜ: HTML'de kullanılan diğer değişkenleri tanımlıyoruz
  confirmPassword: string = '';
  isLoading: boolean = false;
  errorMessage: string = '';

  // HATA ÇÖZÜMÜ: (ngSubmit)="onSignup(signupForm)" metodu
  onSignup(form: NgForm): void {
    if (form.invalid || this.user.password !== this.confirmPassword) {
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    // Simüle edilmiş kayıt işlemi
    setTimeout(() => {
      this.isLoading = false;
      console.log('Kayıt başarılı:', this.user);
      alert('Account created successfully!');
    }, 2000);
  }

  // HATA ÇÖZÜMÜ: (click)="goToLogin($event)" metodu
  goToLogin(event: Event): void {
    event.preventDefault();
    console.log('Login sayfasına yönlendiriliyor...');
    // Buraya router.navigate eklenebilir
  }
}
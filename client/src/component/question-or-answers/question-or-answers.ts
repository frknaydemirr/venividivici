// question-or-answers.ts
import { Component, inject } from '@angular/core'; 
import { Router } from '@angular/router';
import { AuthService } from '../../app/services/auth';


@Component({
  selector: 'app-question-or-answers',
  templateUrl: './question-or-answers.html',
  styleUrl: './question-or-answers.css'
})
export class QuestionOrAnswers {
  private authService = inject(AuthService);
  private router = inject(Router);

  onSubmitAnswer() {
    // isAuthenticated bir metod olduğu için () eklenmelidir
    if (this.authService.isAuthenticated()) {
      // Kullanıcı login, cevabı API'ye gönder
      this.sendAnswerToApi();
    } else {
      // Kullanıcı login değil, giriş sayfasına zorla
      this.router.navigate(['/login']);
    }
  }

  sendAnswerToApi() {
    console.log("Cevap gönderiliyor...");
    // API isteği kodlarınız buraya gelecek
  }
}
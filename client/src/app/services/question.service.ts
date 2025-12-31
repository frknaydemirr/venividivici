import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Question } from '../../models/questions.model';
import { host } from '../constant';

@Injectable({
  providedIn: 'root',
})
export class QuestionService {
  // Swagger'a göre temel URL: http://localhost:8000
  private apiUrl = `${host}/questions`;
  private subscriptionUrl = `${host}/subscriptions`; // Abonelikler için yeni temel URL

  constructor(private http: HttpClient) {}

  // 1. Ana sayfadaki "Hot Questions" (Most Answered)
  getHotQuestions(offset: number = 0, limit: number = 5): Observable<Question[]> {
    const params = new HttpParams()
      .set('offset', offset.toString())
      .set('count', limit.toString()); // Swagger'da 'count' kullanılmış

    return this.http.get<Question[]>(`${this.apiUrl}/most-answered`, { params });
  }

  // 2. ABONELİKLERDEN GELEN SORULAR (Yeni Endpoint Yapısı)
  // Swagger görseline göre: GET /subscriptions/questions
  getSubscribedQuestions(offset: number = 0, limit: number = 5): Observable<Question[]> {
    const params = new HttpParams()
      .set('offset', offset.toString())
      .set('limit', limit.toString());

    // NOT: Swagger'da path içinde userId görünmüyor, bu yüzden kaldırıldı.
    // Eğer kimlik doğrulama gerekiyorsa, bu genellikle Header (api-key) ile yapılır.
    return this.http.get<Question[]>(`${this.subscriptionUrl}/questions`, { params });
  }

  // 3. Şehir sayfasındaki "Recent Questions"
  getRecentQuestionsByCity(cityId: number, offset: number = 0, limit: number = 5): Observable<Question[]> {
    const params = new HttpParams()
      .set('offset', offset.toString())
      .set('limit', limit.toString());

    return this.http.get<Question[]>(`${this.apiUrl}/recent/by-city/${cityId}`, { params });
  }
}
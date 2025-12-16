import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Question } from '../../models/questions.model';

@Injectable({
  providedIn: 'root',
})
export class QuestionService {
  private apiUrl = 'https://api.example.com'; // Kendi API URL'imiz 

  constructor(private http: HttpClient) {}

  // 1. Ana sayfadaki "Hot Questions" için (Most Answered)
  getHotQuestions(offset: number = 0, limit: number = 5): Observable<Question[]> {
    const params = new HttpParams()
      .set('offset', offset.toString())
      .set('count', limit.toString()); // Swagger'da 'count' olarak belirtilmiş

    return this.http.get<Question[]>(`${this.apiUrl}/questions/most-answered`, { params });
  }

  // 2. Ana sayfadaki "Questions from Subscriptions" için
  getSubscribedQuestions(userId: number, offset: number = 0, limit: number = 5): Observable<Question[]> {
    const params = new HttpParams()
      .set('offset', offset.toString())
      .set('limit', limit.toString());

    return this.http.get<Question[]>(`${this.apiUrl}/subscriptions/questions/${userId}`, { params });
  }

  // 3. Şehir sayfasındaki "Recent Questions" (Son Sorular) için
  getRecentQuestionsByCity(cityId: number, offset: number = 0, limit: number = 5): Observable<Question[]> {
    const params = new HttpParams()
      .set('offset', offset.toString())
      .set('limit', limit.toString());

    return this.http.get<Question[]>(`${this.apiUrl}/questions/recent/by-city/${cityId}`, { params });
  }
}
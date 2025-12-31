import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Question } from '../../models/questions.model';
import { host } from '../constant';
@Injectable({
  providedIn: 'root',
})
export class QuestionService {
  private apiUrl = `${host}/questions`;

  constructor(private http: HttpClient) {}

  // 1. Ana sayfadaki "Hot Questions" için (Most Answered)
  getHotQuestions(offset: number = 0, limit: number = 5): Observable<Question[]> {
    const params = new HttpParams()
      .set('offset', offset.toString())
      .set('count', limit.toString()); // Swagger'da 'count' olarak belirtilmiş

    return this.http.get<Question[]>(`${this.apiUrl}/most-answered`, { params });
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

    return this.http.get<Question[]>(`${this.apiUrl}/recent/by-city/${cityId}`, { params });
  }
}
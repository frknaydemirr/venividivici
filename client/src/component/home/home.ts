import { Component, OnInit } from '@angular/core';
import { City } from '../../models/city.model';
import { Country } from '../../models/country.model';
import { CityService } from '../../app/services/city.service';
import { CountryService } from '../../app/services/country.service';
import { CommonModule } from '@angular/common';
import { Question } from '../../models/questions.model';
import { QuestionService } from '../../app/services/question.service';

@Component({
  selector: 'app-home',
  imports: [CommonModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit {

  // Şehirler için veriler ve sayfalama bilgileri
  mostConqueredCities: City[] = [];
  cityOffset=0;
  cityLimit=5;
  hasMoreCities=true;
// Ülkeler için veriler
  mostConqueredCountries: Country[] = [];

  hotQuestions:Question[]=[];
  subscriptionQuestions:Question[]=[];

  constructor(
  private cityService: CityService, 
  private countryService: CountryService,
  private questionService: QuestionService
  ) {}


ngOnInit(): void {
    this.loadMostConqueredCities();
    this.loadMostConqueredCountries();
    this.loadHotQuestions();
    
    // Swagger'da path parametresi olmadığı için userId gönderilmiyor
    this.loadSubscriptionQuestions(); 
}

  //cities
loadMostConqueredCities(): void {
    if (!this.hasMoreCities) return;
//HttpClient Request -> queue
    this.cityService.getMostConqueredCities(this.cityOffset, this.cityLimit)
      .subscribe({
        //data come and assign to mostConqueredCities array -> next step next method:
        next: (newCities: City[]) => { //event handler 
          this.mostConqueredCities = [...this.mostConqueredCities, ...newCities];
          
          if (newCities.length < this.cityLimit) {
            this.hasMoreCities = false; // Son sayfadayız
          }
          this.cityOffset += this.cityLimit; // Bir sonraki sayfanın başlangıcını ayarla
        },
        error: (err) => console.error('Most Conquered Cities yüklenirken hata oluştu:', err)
      });
      //Notes: Promise has include just one event But Observable has include multiple event -> next, error, complete 
  }

//countries
loadMostConqueredCountries(): void {
    this.countryService.getMostConqueredCountries()
      .subscribe({
        next: (countries: Country[]) => {
          this.mostConqueredCountries = countries; 
        },
        error: (err) => console.error('Most Conquered Countries yüklenirken hata oluştu:', err)
      });
  }

  //questions:
loadHotQuestions(): void {
    this.questionService.getHotQuestions(0, 5) // Swagger: /questions/most-answered
      .subscribe({
        next: (questions: Question[]) => {
          this.hotQuestions = questions;
        },
        error: (err) => console.error('Hot questions error:', err)
      });
  }

// Metodun imzasını Swagger'a göre parametresiz hale getiriyoruz
loadSubscriptionQuestions(): void {
  // QuestionService içindeki getSubscribedQuestions artık userId istemiyor
  this.questionService.getSubscribedQuestions(0, 5) 
    .subscribe({
      next: (questions: Question[]) => {
        this.subscriptionQuestions = questions;
      },
      error: (err) => console.error('Subscription questions error:', err)
    });
  }






  

}

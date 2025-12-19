import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { City } from '../../models/city.model';
import { CityService } from '../../app/services/city.service';


@Component({
  selector: 'app-cities',
  standalone: true, 
  imports: [
    
    CommonModule
  ],
  templateUrl: './cities.html',
  styleUrl: './cities.css',
})
export class Cities  implements  OnInit {
  selectedCity?: City;
  isLoading: boolean = true;

constructor(
    private route: ActivatedRoute,
    private cityService: CityService
  ) {}

  //page loaded : -> What happens when the pages  loaded ->we use it ngOnit for that
  ngOnInit(): void {
   this.route.params.subscribe(params => {
    const id= +params['id']; // get the cityId from URL:
    if(id){
      this.loadCityDetails(id); //start to load city details
    }
    });
  }

  search: string = ''; 





  loadCityDetails(id:number):void{
    this.isLoading=true;
    this.cityService.getCityById(id).subscribe({
      next:(city:City)=>{
        this.selectedCity=city;
        this.isLoading=false;

  },
  error:(err)=>{
    console.error('An Error occured while city details loading', err);
    this.isLoading=false;
  }
    });
  }
}

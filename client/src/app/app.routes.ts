import { Layouts } from '../component/layouts/layouts';
import { Routes } from '@angular/router';
import { Home } from '../component/home/home';


export const routes: Routes = [
 
  {
    path: '', 
    component: Layouts,
    children: [
      // 1.1. **Ana Sayfa İçeriği**
      // Layouts içindeki '<router-outlet>' içine 'HomeComponent' yüklenir.
      {
        path: '', // '/' yolu
        component: Home,
        title: 'Anasayfa'
      },
      

      
    ],
  },
  


  
];
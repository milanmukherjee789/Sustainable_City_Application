import { LandingPageComponent } from './landing-page/landing-page.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { CommonModule } from '@angular/common';
import { Map2Component } from './map2/map2.component';
import { RecommendationComponent } from './recommendation/recommendation.component';
import { OldRecommendationsComponent } from './old-recommendations/old-recommendations.component';
import { CreateRecommendationComponent } from './create-recommendation/create-recommendation.component';
import { ReactiveFormsModule } from '@angular/forms';

const routes: Routes = [
  {path: '',   redirectTo: '/login', pathMatch: 'full'},
  {path: 'login', component: LoginComponent},
  {path: 'landing-page', component: LandingPageComponent},
  {path: 'recommendation', component: RecommendationComponent},
  {path: 'old-recommendations', component: OldRecommendationsComponent},
  {path: 'create-recommendation', component: CreateRecommendationComponent},
  {path: 'map2', component: Map2Component},

];

@NgModule({
  imports: [RouterModule.forRoot(routes), CommonModule, ReactiveFormsModule,    CommonModule,  ],
  exports: [RouterModule, ReactiveFormsModule,]
})
export class AppRoutingModule { }
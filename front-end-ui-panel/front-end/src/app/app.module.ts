import { NgModule, isDevMode } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { HttpClientModule } from '@angular/common/http';
import { RecommendationComponent } from './recommendation/recommendation.component';
import { OldRecommendationsComponent } from './old-recommendations/old-recommendations.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms'; // <-- Import the FormsModule
import { CommonModule, NgIf } from '@angular/common';
import { Map2Component } from './map2/map2.component'; // <-- Add this line
import { Router } from 'express';
import { AppRoutingModule } from './app-routing.module';
import { CreateRecommendationComponent } from './create-recommendation/create-recommendation.component';
import { LoginComponent } from './login/login.component';
@NgModule({
  declarations: [
    AppComponent,
    LandingPageComponent,
    OldRecommendationsComponent,
    RecommendationComponent,
    Map2Component,
    LoginComponent,
    CreateRecommendationComponent,
  ],
  imports: [
    AppRoutingModule,
    FormsModule,
    NgIf,
    BrowserModule,
    BrowserAnimationsModule,
    RouterModule.forRoot([
      {path: '',   redirectTo: '/login', pathMatch: 'full'},
      {path: 'login', component: LoginComponent},
      {path: 'landing-page', component: LandingPageComponent},
      {path: 'recommendation', component: RecommendationComponent},
      {path: 'old-recommendations', component: OldRecommendationsComponent},
      {path: 'create-recommendation', component: CreateRecommendationComponent},
      {path: 'map2', component: Map2Component},
    ]),
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    CommonModule // <-- Add this line // <-- Add the FormsModule to the imports array
  ],
  providers: [],
  bootstrap: [AppComponent],
  exports: [AppRoutingModule,RouterModule, ReactiveFormsModule,],
})
export class AppModule { }

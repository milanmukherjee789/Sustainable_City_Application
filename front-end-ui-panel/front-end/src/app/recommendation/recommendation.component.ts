import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs';
import { hostname } from '../model/constants';


@Component({
  selector: 'recommendation',
  templateUrl: './recommendation.component.html',
  styleUrls: ['./recommendation.component.scss']
})

export class RecommendationComponent implements OnInit {
  recommendations: any[] = [];
  incident: string = '';
  location: string = '';
  message: string = '';

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.fetchRecommendations();

}

  fetchRecommendations() {
    this.http.get<any[]>('http://' + hostname + ':5000/recommendations/newrecommendations').subscribe(data => {
      this.recommendations = data;
    }, error => {
      console.error('Error fetching recommendations:', error);
    });
  }

  createRecommendation() {
    const apiEndpoint = 'http://' + hostname + ':5000/recommendations/create';
  
    this.http.post(apiEndpoint, {
      incident: this.incident,
      location: this.location,
      message: this.message
    }).subscribe(() => {
      this.fetchRecommendations(); // Update recommendations after creating a new one
    }, error => {
      console.error('Error creating recommendation:', error);
    });
  }

  onArchive(recommendation: { id: number; incident: string; location: string; message: string; }) {
    // Remove the archived recommendation from the recommendations array
    this.recommendations = this.recommendations.filter(item => item.id !== recommendation.id);
  }
  

  onDelete(recommendation: { id: number; }) {
    // Replace with the actual API endpoint for deleting recommendations
    const apiEndpoint = 'http://' + hostname + ':5000/recommendations/delete';

    this.http.delete(apiEndpoint + '/' + recommendation.id).subscribe(() => {
      this.fetchRecommendations(); // Update recommendations after deleting
    }, error => {
      console.error('Error deleting recommendation:', error);
    });
  }
}
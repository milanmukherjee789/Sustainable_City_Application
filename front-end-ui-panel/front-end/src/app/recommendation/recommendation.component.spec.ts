import { HttpClientModule } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecommendationComponent } from './recommendation.component';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { hostname } from '../model/constants';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterTestingModule } from '@angular/router/testing';
import { AccountService, AlertService } from '../service';

describe('RecommendationComponent', () => {
  let component: RecommendationComponent;
  let fixture: ComponentFixture<RecommendationComponent>;
  let httpMock: HttpTestingController;
  let mockAccountService: jasmine.SpyObj<AccountService>;
  let mockAlertService: jasmine.SpyObj<AlertService>;

  
  beforeEach(async () => {
    mockAccountService = jasmine.createSpyObj('AccountService', ['login']);
    mockAlertService = jasmine.createSpyObj('AlertService', ['clear']);

    await TestBed.configureTestingModule({
      imports: [ReactiveFormsModule, RouterTestingModule,   
        HttpClientTestingModule, FormsModule,],
      declarations: [RecommendationComponent ],
      providers: [
        { provide: AccountService, useValue: mockAccountService },
        { provide: AlertService, useValue: mockAlertService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(RecommendationComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  it('should show map', () => {
    expect(component).toBeTruthy();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should fetch recommendations on init', () => {
    const mockRecommendations = [
      { id: 1, incident: 'incident1', location: 'location1', message: 'message1' },
      { id: 2, incident: 'incident2', location: 'location2', message: 'message2' }
    ];

    component.ngOnInit();

    const req = httpMock.expectOne('http://' + hostname + ':9090/recommendations/newrecommendations');
    expect(req.request.method).toBe('GET');
    req.flush(mockRecommendations);

    expect(component.recommendations).toEqual(mockRecommendations);
  });

  it('should handle error when fetching recommendations', () => {
    spyOn(console, 'error');

    component.ngOnInit();

    const req = httpMock.expectOne('http://' + hostname + ':9090/recommendations/newrecommendations');
    expect(req.request.method).toBe('GET');
    req.flush(null, { status: 500, statusText: 'Internal Server Error' });

    expect(console.error).toHaveBeenCalledWith('Error fetching recommendations:', jasmine.any(Object));
  });

  it('should create a new recommendation', () => {
    component.incident = 'newIncident';
    component.location = 'newLocation';
    component.message = 'newMessage';

    component.createRecommendation();

    const req = httpMock.expectOne('http://' + hostname + ':9090/recommendations/create');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({
      incident: 'newIncident',
      location: 'newLocation',
      message: 'newMessage'
    });
  });

  it('should handle error when creating a new recommendation', () => {
    spyOn(console, 'error');

    component.createRecommendation();

    const req = httpMock.expectOne('http://' + hostname + ':9090/recommendations/create');
    expect(req.request.method).toBe('POST');
    req.flush(null, { status: 500, statusText: 'Internal Server Error' });

    expect(console.error).toHaveBeenCalledWith('Error creating recommendation:', jasmine.any(Object));
  });

  it('should archive a recommendation', () => {
    component.recommendations = [
      { id: 1, incident: 'incident1', location: 'location1', message: 'message1' },
      { id: 2, incident: 'incident2', location: 'location2', message: 'message2' }
    ];

    component.onArchive({ id: 1, incident: '', location:'', message:'' });
    
    expect(component.recommendations).toEqual([
      { id: 2, incident: 'incident2', location:'location2', message:'message2' }
    ]);
  });

  it('should delete a recommendation', () => {
    component.onDelete({ id: 1 });

    const req = httpMock.expectOne('http://' + hostname + ':9090/recommendations/delete/1');
    expect(req.request.method).toBe('DELETE');
  });

  it('should handle error when deleting a recommendation', () => {
    spyOn(console, 'error');

    component.onDelete({ id: 1 });

    const req = httpMock.expectOne('http://' + hostname + ':9090/recommendations/delete/1');
    expect(req.request.method).toBe('DELETE');
    
req.flush(null, { status: 500, statusText:'Internal Server Error' });
    
expect(console.error).toHaveBeenCalledWith('Error deleting recommendation:', jasmine.any(Object));
});
});

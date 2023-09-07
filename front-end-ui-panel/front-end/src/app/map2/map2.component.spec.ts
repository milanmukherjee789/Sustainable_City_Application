import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { FormsModule } from '@angular/forms';
import { Map2Component } from './map2.component';
import * as L from 'leaflet';

describe('Map2Component', () => {
  let component: Map2Component;
  let fixture: ComponentFixture<Map2Component>;
  let mapContainer: HTMLElement;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HttpClientTestingModule, FormsModule],
      declarations: [Map2Component],
    }).compileComponents();
  });

  beforeEach(() => {
    // Create a new DOM element for the map container
    mapContainer = document.createElement('div');
    mapContainer.id = 'mapid';
    document.body.appendChild(mapContainer);

    fixture = TestBed.createComponent(Map2Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  afterEach(() => {
    // Clean up the DOM element after each test
    document.body.removeChild(mapContainer);
  });

  it('should initialize the map', () => {
    // Removed the unnecessary ngOnInit call
    expect(component.map).toBeDefined();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should have busRoutes, luasRoutes, and taxiRoutes as empty arrays', () => {
    expect(Array.isArray(component.busRoutes)).toBe(true);
    expect(component.busRoutes.length).toBe(0);

    expect(Array.isArray(component.luasRoutes)).toBe(true);
    expect(component.luasRoutes.length).toBe(0);

    expect(Array.isArray(component['taxiRoutes'])).toBe(true);
    expect(component['taxiRoutes'].length).toBe(0);
  });
});

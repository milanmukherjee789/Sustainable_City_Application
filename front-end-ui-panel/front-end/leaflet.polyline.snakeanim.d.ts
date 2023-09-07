import * as L from 'leaflet';

declare module 'leaflet' {
  namespace Polyline {
    interface SnakeAnim {
      snakeIn(options?: any): void;
    }

    function snakeIn(coords: LatLngExpression[], options?: any): Polyline;
  }

  interface PolylineOptions {
    snakingSpeed?: number;
    snakingPause?: number;
    snakingReverse?: boolean;
    snakingDir?: 'normal' | 'reverse' | 'toggle';
  }

  interface Polyline {
    snakeIn: (options?: PolylineOptions) => void;
  }
}

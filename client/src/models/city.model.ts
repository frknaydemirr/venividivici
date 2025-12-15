import { url } from "inspector";

export interface City{
    'city-id': number;
    'city-name': string;
    url: string;
    info: string;
}
// API'den dönen liste yapısı
export interface CityListResponse extends Array<City>{}
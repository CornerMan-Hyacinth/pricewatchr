export interface User {
  id?: string;
  name: string;
  email: string;
  email_verified: boolean;
  role: "user" | "admin";
  created_at?: string;
}

export interface Product {
  id?: string;
  user_id: string;
  name: string;
  target_price?: number;
  current_price?: number;
  last_checked?: string;
  added_at?: string;
}

export interface ProductUrl {
  id?: string;
  product: string;
  url: string;
  is_primary: boolean;
  retailer?: string;
}

export interface PriceHistory {
  id?: string;
  product_id: string;
  product_url_id: string;
  price: number;
  recorded_at: string;
}

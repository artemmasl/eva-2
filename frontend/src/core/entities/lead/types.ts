export type LeadKind = 'callback' | 'consultation' | 'booking' | 'conditions';
export type LeadStatus = 'new' | 'in_progress' | 'done';

export interface LeadCreate {
  kind: LeadKind;
  name?: string;
  phone: string;
  comment?: string;
  developer_slug?: string;
  complex_id?: string | null;
  space_id?: string | null;
  source_url?: string;
}

export interface Lead extends LeadCreate {
  id: string;
  status: LeadStatus;
  created_at: string;
}

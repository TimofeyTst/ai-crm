-- Add media_type column to resumes table
-- depends: 0002_create_resumes_table

ALTER TABLE resumes ADD COLUMN media_type VARCHAR(50) NOT NULL;

CREATE INDEX idx_resumes_media_type ON resumes(media_type);


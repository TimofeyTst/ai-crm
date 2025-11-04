-- Create resumes table for storing resume file metadata
-- depends: 0001_initial

CREATE TABLE resumes (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- File metadata
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100) NOT NULL DEFAULT 'application/pdf',
    
    -- Storage metadata
    storage_path VARCHAR(500) NOT NULL,
    storage_type VARCHAR(50) NOT NULL DEFAULT 'local',
    
    -- Resume metadata
    title VARCHAR(255),
    description TEXT,
    
    -- Status
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_resumes_is_active ON resumes(is_active);
CREATE INDEX idx_resumes_created_at ON resumes(created_at);

-- Trigger function to update updated_at on row update
CREATE OR REPLACE FUNCTION trigger_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for updated_at column
CREATE TRIGGER set_updated_at_on_resumes
BEFORE UPDATE ON resumes
FOR EACH ROW
EXECUTE FUNCTION trigger_updated_at();

CREATE TRIGGER set_updated_at_on_users
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION trigger_updated_at();

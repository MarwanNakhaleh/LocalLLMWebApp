from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Context(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_text = db.Column(db.String, nullable=False)
    index_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Context(id={self.id},full_text='{self.full_text}',index_name='{self.index_name}')"

class StoredDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String, nullable=False)
    secure_filename = db.Column(db.String, nullable=False)
    sequence_number = db.Column(db.Integer, nullable=False)
    context_id = db.Column(db.Integer, db.ForeignKey('context.id'), nullable=False)

    context = db.relationship('Context', backref=db.backref('stored_documents', lazy=True))

    def __repr__(self):
        return f"StoredDocument(id={self.id},hash='{self.hash}',secure_filename='{self.secure_filename}',sequence_number='{self.sequence_number}',context_id={self.context_id})"
    
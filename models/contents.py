from tortoise import models,  fields

class Contents(models.Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    content_type = fields.CharField(max_length=50)
    title = fields.CharField(max_length=255)

    def __str__(self):
        return self.title
    
class QRCodes(models.Model):
    id = fields.IntField(pk=True)
    scan_id = fields.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.scan_id if self.scan_id else "QR Code {}".format(self.id)

class Scans(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='scans')
    content = fields.ForeignKeyField('models.Contents', related_name='scans')
    qrcode = fields.ForeignKeyField('models.QRCodes', related_name='scans')

    def __str__(self):
        return "Scan {} by User {}".format(self.id, self.user_id)
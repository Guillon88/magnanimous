
from django.contrib.gis.db import models
from django.db.models.signals import post_delete, post_save
from django.contrib.auth import get_user_model
from stream_django.activity import Activity
from stream_django.feed_manager import feed_manager


class BaseModel(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

class Item(BaseModel):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE, null=True)
    pin_count = models.IntegerField(default=0)
    fecha = models.DateField()
    IP = "IP"
    IM = "IM"
    IG = "IG"
    TIPO_CHOICES = (
        (IP, "Incendio Pequeño"),
        (IM, "Incendio Mediano"),
        (IG, "Incendio Grande"),
    )
    tipo = models.CharField(max_length=4,
                            choices=TIPO_CHOICES,
                            default=IP)

    mpoly = models.MultiPolygonField(null=True)
    foco = models.PointField(null=True)

class Pin(Activity, BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    influencer = models.ForeignKey(
        get_user_model(),
                             on_delete=models.CASCADE, related_name='influenced_pins')
    message = models.TextField(blank=True, null=True)

    @classmethod
    def activity_related_models(cls):
        return ['user', 'item']

    @property
    def activity_object_attr(self):
        return self

    @property
    def extra_activity_data(self):
        return dict(item_id=self.item_id)

def soft_delete(sender, instance, **kwargs):
    if instance.deleted_at is not None:
        feed_manager.activity_delete(sender, instance, **kwargs)

post_save.connect(soft_delete, sender=Pin)


class Follow(Activity, BaseModel):
    '''
    A simple table mapping who a user is following.
    For example, if user is Kyle and Kyle is following Alex,
    the target would be Alex.
    '''
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE, related_name='following_set')
    target = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE, related_name='follower_set')

    @classmethod
    def activity_related_models(cls):
        return ['user', 'target']

    @property
    def activity_object_attr(self):
        return self

    @property
    def activity_notify(self):
        target_feed = feed_manager.get_notification_feed(self.target_id)
        return [target_feed]


def follow_change(sender, instance, created, **kwargs):
    if instance.deleted_at is None:
        feed_manager.follow_user(instance.user_id, instance.target_id)
    else:
        feed_manager.unfollow_user(instance.user_id, instance.target_id)


def unfollow_feed(sender, instance, **kwargs):
    feed_manager.unfollow_user(instance.user_id, instance.target_id)


post_save.connect(follow_change, sender=Follow)
post_delete.connect(unfollow_feed, sender=Follow)

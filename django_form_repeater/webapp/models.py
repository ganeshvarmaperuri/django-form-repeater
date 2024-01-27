from django.db import models


GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
)


class GrandParent(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER, max_length=50)
    age = models.CharField(max_length=10)
    img = models.ImageField(upload_to="photos/", default="profile_pic.png", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    @property
    def get_child(self):
        return list(self.parent_grandparent.all())


class Parent(models.Model):
    parent = models.ForeignKey(GrandParent, on_delete=models.CASCADE, related_name="parent_grandparent")
    name = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER, max_length=50)
    age = models.CharField(max_length=10)
    img = models.ImageField(upload_to="photos/", default="profile_pic.png", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    @property
    def get_child(self):
        return list(self.child.all())


class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="child")
    name = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER, max_length=50)
    age = models.CharField(max_length=10)
    img = models.ImageField(upload_to="photos/", default="profile_pic.png", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def get_child(self):
        return list(self.grandchild_child.all())


class GrandChild(models.Model):
    parent = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="grandchild_child")
    name = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER, max_length=50)
    age = models.CharField(max_length=10)
    img = models.ImageField(upload_to="photos/", default="profile_pic.png", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"



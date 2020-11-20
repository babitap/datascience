from django.contrib import auth
from django.db import models
#from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from api.graphqlapi.model_acara import AcaraSchoolMaster
from functools import reduce
from django.db.models import Q

#------------------------------------------------------------------------------

class Entity(models.Model):
    """
    id: unique id for entity
    entity_name: name of entity
    industry_id: id of entitiy wihtin specific industry
    industry_name: name of industry for entity
    """
    entity_name = models.CharField(max_length=255, null=True)
    industry_id = models.IntegerField(null=False)
    industry_name = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_activated = models.DateTimeField(_('date joined'), default=timezone.now)
    date_disabled = models.DateTimeField(_('date disabled'), default=None, null=True)

    class Meta:
        unique_together = ('industry_id', 'industry_name',)

#------------------------------------------------------------------------------

class PermissionManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, codename, app_label, model):
        return self.get(
            codename=codename,
            #content_type=ContentType.objects.db_manager(self.db).get_by_natural_key(app_label, model),
        )

class Permission(models.Model):

    name = models.CharField(_('name'), max_length=255)
    codename = models.CharField(_('codename'), max_length=100, unique=True)
    is_findex = models.BooleanField(default=False)
    is_findex_all = models.BooleanField(default=False)
    is_accessible = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this permission should be treated as active. '
            'Unselect this instead of deleting permission.'
        ),
    )
    objects = PermissionManager()

    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        #unique_together = (('codename'),)
        #ordering = ('content_type__app_label', 'content_type__model',
        #            'codename')

    '''def __str__(self):
                    return "%s | %s | %s" % (
                        self.content_type.app_label,
                        self.content_type,
                        self.name,
                    )'''

    '''def natural_key(self):
                    return (self.codename,) + self.content_type.natural_key()
                natural_key.dependencies = ['contenttypes.contenttype']'''

#------------------------------------------------------------------------------

class GroupManager(models.Manager):
    """
    The manager for the auth's Group model.
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)

class EntityGroup(models.Model):

    name = models.CharField(_('name'), max_length=80)
    description = models.CharField(_('description'), max_length=255)
    entity = models.ForeignKey(Entity, db_index=True, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this entity group should be treated as active. '
            'Unselect this instead of deleting groups.'
        ),
    )

    objects = GroupManager()

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        unique_together = ('name', 'entity',)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

#-----------------------------------------------------------------------------
class ReportCategoryManager(models.Manager):
    """
    The manager for the report category model.
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)

class ReportCategory (models.Model):
    name = models.CharField(_('name'), max_length=80, null=False)
    description = models.CharField(_('description'), max_length=255)

    objects = ReportCategoryManager()

    class Meta:
        verbose_name = _('report category')
        verbose_name_plural = _('report categories')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


#------------------------------------------------------------------------------
class ReportManager(models.Manager):
    """
    The manager for the report model.
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Report (models.Model):

    name = models.CharField(_('name'), max_length=255, null=False)
    codename = models.CharField(_('codename'), max_length=100, unique=True)
    workspace_id = models.CharField(_('workspaceId'), max_length=36, null=False)
    report_id = models.CharField(_('reportId'), max_length=36, null=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=False)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, null=False)
    category = models.ForeignKey(ReportCategory, on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this report should be treated as active. '
            'Unselect this instead of deleting report.'
        ),
    )
    objects = ReportManager()

    class Meta:
        verbose_name = _('report')
        verbose_name_plural = _('reports')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

#------------------------------------------------------------------------------

class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, **extra_fields):

        if not username:
            raise ValueError('The given username must be set')
        username = self.normalize_email(username)
        user=self.model(
            username = username,
            **extra_fields
            )
        user.save(using=self._db)
        return user

    def create_user(self, username, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, **extra_fields)

    def create_superuser(self, username, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, **extra_fields)

    def create_findexuser(self, username, **extra_fields):
        extra_fields.setdefault('is_findex', True)
        if extra_fields.get('is_findex') is not True:
            raise ValueError('Findex user must have is_findex=True.')
        return self._create_user(username, **extra_fields)

    def create_findexuser_all(self, username, **extra_fields):
        extra_fields.setdefault('is_findex_all', True)
        if extra_fields.get('is_findex_all') is not True:
            raise ValueError('Findex "all" user must have is_findex_all=True.')
        return self._create_user(username, **extra_fields)

# A few helper functions for common logic between User and AnonymousUser.
def _user_get_all_permissions(user, obj):
    permissions = set()
    for backend in auth.get_backends():
        if hasattr(backend, "get_all_permissions"):
            permissions.update(backend.get_all_permissions(user, obj))
    return permissions

def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False

def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False

class PermissionsMixin(models.Model):
    """
    Add the fields and methods necessary to support the Group and Permission
    models using the ModelBackend.
    """
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    groups = models.ManyToManyField(
        EntityGroup,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )
    entities = models.ManyToManyField(
        Entity,
        verbose_name=_('entities'),
        blank=True,
        help_text=_(
            'The entities this user belongs to.'
        ),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, entityId=None, obj=None):
        """
        If user has either is_superuser, is_findex or is_findex_all set
        Simply return permissions for given user

        For all other user, only the permissions granted to the group
        where user belongs to will be returned. If entityId is provided
        only the permissions for the entity groups in that particular entity
        will be returned.  
        """
        if self.is_active:
            isActiveFiler = Q(is_active=True)
            if self.is_superuser:
                return list(Permission.objects.filter(isActiveFiler).values('id', 'codename', 'name'))
            else:
                filter = None
                if self.is_findex:
                    filter = Q(is_findex=1)
                elif self.is_findex_all:
                    filter = Q(is_findex_all=1)
                else:
                    group_list = None
                    if entityId is not None:
                        group_list = list(map(lambda x: x['id'], self.groups.filter(entity_id=entityId).values('id')))
                    else:
                        group_list = list(map(lambda x: x['id'], self.groups.values('id')))
                    group_filter = Q(id__in=group_list)
                    filter = Q(id__in=EntityGroup.objects.filter(group_filter).values('permissions'))
                return list(Permission.objects.filter(filter & isActiveFiler).values('id', 'codename', 'name'))
        else:
            return _user_get_all_permissions(self, obj)


    def has_perm(self, perm, entityId=None, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        
        #First check whether user is active
        if self.is_active:
            # Active superusers have all permissions.
            if self.is_superuser:
                return True
            else:
                permissions = self.get_all_permissions(entityId, obj)
                permission_codes = list(map(lambda x: x['codename'], permissions))
                return perm in permission_codes
        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_superuser_perm(self, obj=None): 
        if self.is_active and self.is_superuser: 
            return True
        else: 
            return False 

    def has_special_user_perm(self, obj=None):
        if self.is_active and (self.is_superuser or self.is_findex_all or self.is_findex ): 
            return True
        else: 
            return False                 

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def get_entities(self):
        query = None

        if self.has_perm('view_all_schools'):
            query = Entity.objects.filter(is_active=True)
        else:
            query = self.entities.filter(is_active=True)
        
        return list(query.values('id', 'industry_id', 'entity_name', 'industry_name').order_by('id'))

    def get_entity_industryIds(self):
        industryIds = list(self.entities.filter(is_active=True).values('industry_id'))
        return list(map(lambda x: x['industry_id'], industryIds))

    def get_default_school(self):
        entity_list = self.get_entity_industryIds()

        defaultEntity = []

        if self.has_perm('view_all_schools'):
            firstEntity = Entity.objects.filter(is_active=True).values('industry_id').order_by('id').first()
            defaultEntity.append(firstEntity['industry_id'])
        else:
            defaultEntity = entity_list

        q_list = map(lambda n: Q(acara_id__iexact=n), defaultEntity)
        q_list = reduce(lambda a, b: a | b, q_list)
        default_school = AcaraSchoolMaster.objects.using('public_data').get(acara_id=defaultEntity[0])
        return default_school

class User(AbstractBaseUser,PermissionsMixin):
    """
    All fields stored based on the user
    id: is in base model and is referred as user_id for app - unique in this model
    oid: this id is from B2C and should be filled on first login
    """
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    given_name = models.CharField(max_length=150, null=True)
    family_name = models.CharField(max_length=150, null=True)
    oid = models.CharField(max_length=255, blank=True, null=True)
    is_findex = models.BooleanField(default=False)
    is_findex_all = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    date_disabled = models.DateTimeField(_('date disabled'), default=None, null=True)
    created_by = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING)
    last_selected_entity = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True, related_name='last_selected_entity')

    objects=MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
import csv
from django.http import HttpResponse
from datetime import datetime

def export_to_csv(modeladmin, request, queryset):
    """Exporting queryset results and filter into CSV"""
    # limit only staff and super_user accounts
    if request.user.is_staff or request.user.is_superuser:
        if queryset.count() > 0:
            # generate response and filename
            response = HttpResponse(mimetype="text/csv")
            today = datetime.now().strftime("%Y-%M-%d_%H:%M:%S")
            filename = "records-%s.csv" % today
            response["Content-Disposition"] = ('attachment; filename="%s"' %
                                               filename)
            writer = csv.writer(response)

            # Get column name
            columns = ['First name', 'Last_name', 'Email', 'Last login', 'Date joined', 'Email verified', 'Country', 'Language code 1', 'Language code 2']
            # columns = [field.name for field in queryset[0]._meta.fields]
            writer.writerow(columns)

            # Write data
            for obj in queryset:
                columns = ['first_name', 'last_name', 'email', 'last_login', 'date_joined']
                fields = map(lambda x: generate_value(obj, x), columns)
                obj = obj.userprofile
                columns = ['email_verified', 'country', 'language', 'second_language']
                fields2 = map(lambda x: generate_value(obj, x), columns)
                writer.writerow(fields + fields2)

            return response

export_to_csv.short_description = "Export results to CSV"


def generate_value(obj, column):
    """Get fields value and convert to ASCIC for string type"""
    row = getattr(obj, column)
    if isinstance(row, basestring):
        row = row.encode('ascii', 'ignore')
    return row


import subprocess
def dbpush() :
    subprocess.run("prisma db push --schema ./database/schema.prisma")

def migrate():
    subprocess.run("prisma migrate dev --schema ./database/schema.prisma")
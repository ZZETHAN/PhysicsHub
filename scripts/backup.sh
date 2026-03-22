#!/bin/bash
#
# PhysicsHub Backup System
# Usage: bash backup.sh [create|restore|list]
#

BACKUP_DIR="$HOME/Desktop/PhysicsHub_Backups"
SOURCE_DIR="$HOME/Desktop/PhysicsHub"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

create_backup() {
    echo "Creating backup..."
    mkdir -p "$BACKUP_DIR"
    
    # Create tar archive
    tar -czf "$BACKUP_DIR/physicshub_$TIMESTAMP.tar.gz" \
        -C "$SOURCE_DIR" \
        --exclude='.git' \
        .
    
    echo "✅ Backup created: physicshub_$TIMESTAMP.tar.gz"
    
    # Keep only last 5 backups
    cd "$BACKUP_DIR"
    ls -t physicshub_*.tar.gz 2>/dev/null | tail -n +6 | xargs -r rm
    echo "🧹 Old backups cleaned (keeping last 5)"
}

list_backups() {
    echo "Available backups:"
    echo "=================="
    cd "$BACKUP_DIR" 2>/dev/null || { echo "No backups found"; exit 0; }
    
    ls -lt physicshub_*.tar.gz 2>/dev/null | while read line; do
        filename=$(echo "$line" | awk '{print $NF}')
        size=$(echo "$line" | awk '{print $5}')
        date=$(echo "$line" | awk '{print $6, $7, $8}')
        echo "  $filename ($size) - $date"
    done
    
    if [ ! -f "physicshub_*.tar.gz" 2>/dev/null ]; then
        echo "  No backups found"
    fi
}

restore_backup() {
    if [ -z "$2" ]; then
        echo "Usage: bash backup.sh restore [backup_filename]"
        echo ""
        echo "Available backups:"
        list_backups
        exit 1
    fi
    
    BACKUP_FILE="$BACKUP_DIR/$2"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        echo "❌ Backup not found: $2"
        exit 1
    fi
    
    echo "⚠️  WARNING: This will overwrite current PhysicsHub files!"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        # Create emergency backup first
        echo "Creating emergency backup of current state..."
        tar -czf "$BACKUP_DIR/emergency_before_restore_$TIMESTAMP.tar.gz" -C "$SOURCE_DIR" .
        
        # Restore
        echo "Restoring from $2..."
        rm -rf "$SOURCE_DIR"/*
        tar -xzf "$BACKUP_FILE" -C "$SOURCE_DIR"
        echo "✅ Restore complete!"
        echo "💾 Emergency backup created: emergency_before_restore_$TIMESTAMP.tar.gz"
    else
        echo "❌ Restore cancelled"
    fi
}

# Main
case "$1" in
    create|c)
        create_backup
        ;;
    list|l)
        list_backups
        ;;
    restore|r)
        restore_backup "$@"
        ;;
    *)
        echo "PhysicsHub Backup System"
        echo "========================"
        echo ""
        echo "Usage:"
        echo "  bash backup.sh create    - Create new backup"
        echo "  bash backup.sh list      - List all backups"
        echo "  bash backup.sh restore   - Restore from backup"
        echo ""
        echo "Current backups:"
        list_backups
        ;;
esac

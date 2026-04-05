from __future__ import annotations

from typing import TYPE_CHECKING
from threading import Thread

if TYPE_CHECKING:
    from apmodel.base import AS2Model


from apmodel._vendor.type_mapping import TYPE_MAPPING
from apmodel.inference import TypeInferencer

type_loader = TypeInferencer(TYPE_MAPPING)

def _infer_with_timeout(data, context, timeout=10):
    """Try to infer type with a timeout."""
    result = {'model_cls': None}
    
    def infer_thread():
        try:
            result['model_cls'] = type_loader.infer(data, parent_context=context)
        except Exception as e:
            result['error'] = e
    
    thread = Thread(target=infer_thread)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        # Timeout occurred - fallback to direct lookup by type name
        return None
    
    return result.get('model_cls')

def load(
    data: dict, *args: object, context: dict | None = None, **kwargs: object
) -> AS2Model | None:
    if context is None:
        context = data
    
    # Try to infer type with a timeout to prevent hangs
    try:
        model_cls: type[AS2Model] | None = _infer_with_timeout(data, context)
    except Exception:
        model_cls = None
    
    # If type inference timed out or failed, try fallback approaches
    if model_cls is None and isinstance(data, dict):
        # Try to import and get the class directly by type name
        type_name = data.get('type')
        if type_name:
            # Map common types
            type_map = {
                'Note': 'apmodel.objects.note.Note',
                'Document': 'apmodel.objects.document.Document',
                'Hashtag': 'apmodel.objects.hashtag.Hashtag',
                'Emoji': 'apmodel.objects.emoji.Emoji',
                'OrderedCollectionPage': 'apmodel.core.OrderedCollectionPage',
                'OrderedCollection': 'apmodel.core.OrderedCollection',
                'CollectionPage': 'apmodel.core.CollectionPage',
                'Collection': 'apmodel.core.Collection',
                'Link': 'apmodel.core.Link',
                'Object': 'apmodel.core.Object',
            }
            
            if type_name in type_map:
                try:
                    module_name, class_name = type_map[type_name].rsplit('.', 1)
                    module = __import__(module_name, fromlist=[class_name])
                    model_cls = getattr(module, class_name)
                except Exception:
                    pass

    if model_cls is not None:
        return model_cls.model_validate(data, context=context, *args, **kwargs)

    return None
